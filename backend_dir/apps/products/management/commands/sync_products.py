import re
from decimal import Decimal

import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction
from django.db.models import Q

from apps.products.llm import generate_core_info, generate_friendly_label
from apps.products.models import Bank, PreferentialCondition, Product, ProductOption

FSS_BASE_URL = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
# 020000=시중은행(1금융권), 030300=저축은행
TOP_FIN_GRP_NOS = ["020000", "030300"]
GRP_TO_BANK_TYPE = {
    "020000": Bank.BankType.FIRST_TIER,
    "030300": Bank.BankType.SAVINGS,
}
# spcl_cnd 텍스트에서 "0.3%p", "연 0.5 %" 같은 우대금리를 뽑는 패턴.
RATE_PATTERN = re.compile(r"(\d+(?:\.\d+)?)\s*%")


class Command(BaseCommand):
    help = "금감원 API에서 적금 상품을 받아 DB에 적재. --with-llm 시 GMS로 AI 필드 보강"

    def add_arguments(self, parser):
        parser.add_argument(
            "--with-llm",
            action="store_true",
            help="GMS로 friendly_label·difficulty·요약을 채운다(비용 발생)",
        )
        parser.add_argument(
            "--llm-limit",
            type=int,
            default=0,
            help="LLM 보강 대상 행 수 제한(테스트용, 0=제한 없음)",
        )

    def _parse_conditions(self, raw):
        """spcl_cnd 원문을 줄 단위로 쪼개 (label, rate) 목록으로 만든다.

        LLM 없이 텍스트만 처리하는 2차 단계. friendly_label/difficulty는
        나중에 LLM 배치가 채우므로 여기서는 건드리지 않는다(NULL 유지).
        """
        if not raw:
            return []

        results = []
        seen = set()
        for segment in re.split(r"[\n\r]+", raw):  # 줄바꿈으로 조건 분리
            label = segment.strip()[:500]  # 모델 max_length=500
            if not label or label in seen:
                continue
            seen.add(label)
            match = RATE_PATTERN.search(label)
            rate = Decimal(match.group(1)) if match else Decimal("0")
            results.append((label, rate))
        return results

    def _fetch(self, grp_no, page_no):
        res = requests.get(
            FSS_BASE_URL,
            params={
                "auth": settings.FSS_API_KEY,
                "topFinGrpNo": grp_no,
                "pageNo": page_no,
            },
            timeout=30,
        )
        return res.json()["result"]

    def handle(self, *args, **options):
        total_products = 0
        total_options = 0
        total_conditions = 0

        with transaction.atomic():
            for grp_no in TOP_FIN_GRP_NOS:
                bank_type = GRP_TO_BANK_TYPE[grp_no]
                page_no = 1
                while True:
                    data = self._fetch(grp_no, page_no)
                    if data.get("err_cd") != "000":
                        self.stderr.write(f"[{grp_no}] API 오류: {data.get('err_msg')}")
                        break

                    # baseList -> Bank, Product 적재
                    product_map = {}
                    for item in data.get("baseList", []):
                        bank, _ = Bank.objects.update_or_create(
                            bank_code=item["fin_co_no"],
                            defaults={
                                "bank_name": item["kor_co_nm"],
                                "bank_type": bank_type,
                            },
                        )
                        product, _ = Product.objects.update_or_create(
                            bank=bank,
                            fin_prdt_cd=item["fin_prdt_cd"],
                            defaults={
                                "product_name": item["fin_prdt_nm"],
                                "join_member": item.get("join_member") or "",
                                "join_way": item.get("join_way") or "",
                                "max_limit": item.get("max_limit"),
                                "maturity_interest": item.get("mtrt_int") or "",
                                "etc_note": item.get("etc_note") or "",
                                "special_condition_raw": item.get("spcl_cnd") or "",
                                "dcls_strt_day": item.get("dcls_strt_day") or "",
                                "dcls_end_day": item.get("dcls_end_day"),
                            },
                        )
                        product_map[(item["fin_co_no"], item["fin_prdt_cd"])] = product
                        total_products += 1

                        # spcl_cnd 파싱 → PreferentialCondition 적재 (비LLM 2차)
                        parsed = self._parse_conditions(item.get("spcl_cnd") or "")
                        for label, rate in parsed:
                            PreferentialCondition.objects.update_or_create(
                                product=product,
                                label=label,
                                defaults={"rate": rate},
                            )
                        total_conditions += len(parsed)
                        # has_bonus = 우대조건 존재 여부
                        product.has_bonus = bool(parsed)
                        product.save(update_fields=["has_bonus"])

                    # optionList -> ProductOption 적재
                    for opt in data.get("optionList", []):
                        product = product_map.get(
                            (opt["fin_co_no"], opt["fin_prdt_cd"])
                        )
                        if product is None or opt.get("intr_rate") is None:
                            continue
                        ProductOption.objects.update_or_create(
                            product=product,
                            save_term=opt["save_trm"],
                            intr_rate_type=opt["intr_rate_type"],
                            rsrv_type=opt["rsrv_type"],
                            defaults={
                                "base_rate": opt["intr_rate"],
                                "max_rate": opt.get("intr_rate2"),
                            },
                        )
                        total_options += 1

                    if page_no >= data.get("max_page_no", 1):
                        break
                    page_no += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"완료: 상품 {total_products}개, 옵션 {total_options}개, "
                f"우대조건 {total_conditions}개 적재"
            )
        )

        if options["with_llm"]:
            self._enrich_with_llm(options["llm_limit"])

    def _enrich_with_llm(self, limit):
        """NULL인 AI 필드를 GMS로 채운다. 실패 행은 NULL 유지 → 다음 실행 때 재시도."""
        # 1) 우대조건: friendly_label 또는 difficulty가 비어있는 행
        conditions = PreferentialCondition.objects.filter(
            Q(friendly_label__isnull=True) | Q(difficulty__isnull=True)
        )
        if limit:
            conditions = conditions[:limit]

        cond_done = 0
        for cond in conditions:
            friendly, difficulty = generate_friendly_label(cond.label)
            if friendly is None and difficulty is None:
                continue  # 호출 실패 → NULL 유지
            cond.friendly_label = friendly or cond.friendly_label
            cond.difficulty = difficulty or cond.difficulty
            cond.save(update_fields=["friendly_label", "difficulty"])
            cond_done += 1

        # 2) 상품: 요약 3개 중 하나라도 비어있는 행
        products = Product.objects.filter(
            Q(join_summary__isnull=True)
            | Q(maturity_summary__isnull=True)
            | Q(etc_summary__isnull=True)
        )
        if limit:
            products = products[:limit]

        prod_done = 0
        for product in products:
            info = generate_core_info(product)
            if not info:
                continue  # 호출 실패 → NULL 유지
            product.join_summary = info.get("join_summary") or product.join_summary
            product.maturity_summary = (
                info.get("maturity_summary") or product.maturity_summary
            )
            product.etc_summary = info.get("etc_summary") or product.etc_summary
            product.save(
                update_fields=["join_summary", "maturity_summary", "etc_summary"]
            )
            prod_done += 1

        self.stdout.write(
            self.style.SUCCESS(
                f"LLM 보강: 우대조건 {cond_done}개, 상품 {prod_done}개 갱신"
            )
        )
