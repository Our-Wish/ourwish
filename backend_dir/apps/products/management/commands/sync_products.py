import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.products.llm import generate_ai_summary, generate_tags
from apps.products.models import Bank, Product, ProductOption

FSS_BASE_URL = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
# 020000=시중은행(1금융권), 030300=저축은행
TOP_FIN_GRP_NOS = ["020000", "030300"]
GRP_TO_BANK_TYPE = {
    "020000": Bank.BankType.FIRST_TIER,
    "030300": Bank.BankType.SAVINGS,
}

# LLM이 채우는 태그·연령 필드(ai_summary는 루프에서 별도로 처리).
_TAG_FIELDS = [
    "tag_salary_transfer",
    "tag_auto_transfer",
    "tag_card_usage",
    "tag_housing_subscription",
    "age_min",
    "age_max",
]


class Command(BaseCommand):
    help = "금감원 API에서 적금 상품을 받아 DB에 적재. --with-llm 시 GMS로 태그·요약 보강"

    def add_arguments(self, parser):
        parser.add_argument(
            "--with-llm",
            action="store_true",
            help="GMS로 매칭 태그·연령·AI 한줄요약을 채운다(비용 발생)",
        )
        parser.add_argument(
            "--llm-limit",
            type=int,
            default=0,
            help="LLM 보강 대상 상품 수 제한(테스트용, 0=제한 없음)",
        )
        parser.add_argument(
            "--llm-only",
            choices=["tags", "summary"],
            default=None,
            help="LLM 보강을 일부만 수행: tags=태그·연령만, summary=AI요약만 "
            "(생략 시 둘 다). 비용을 나눠 적재할 때 사용.",
        )

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
                        # 우대조건 태그·요약은 LLM 배치(--with-llm)가 따로 채운다.
                        # 여기서는 FSS 원본 필드만 적재한다(spcl_cnd 전문 포함).
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
                f"완료: 상품 {total_products}개, 옵션 {total_options}개 적재"
            )
        )

        if options["with_llm"]:
            self._enrich_with_llm(options["llm_limit"], options["llm_only"])

    def _enrich_with_llm(self, limit, only=None):
        """아직 LLM 처리 안 된 상품의 태그·연령·AI요약을 GMS로 채운다.

        대상은 ai_summary가 NULL인 상품(='미처리' 마커). 실패 시 NULL 유지 → 재시도.
        only=None이면 태그+요약 둘 다, "tags"면 태그·연령만, "summary"면 AI요약만.
        (tags만 돌리면 ai_summary는 NULL로 남으니 나중에 summary만 따로 채울 수 있다.
         단 tags는 별도 마커가 없어 재실행 시 전체 재태깅된다.)
        """
        do_tags = only in (None, "tags")
        do_summary = only in (None, "summary")

        products = Product.objects.filter(ai_summary__isnull=True)
        if limit:
            products = products[:limit]

        done = 0
        for product in products:
            update_fields = []
            if do_tags:
                tags = generate_tags(product)
                if tags:
                    product.tag_salary_transfer = tags["salary_transfer"]
                    product.tag_auto_transfer = tags["auto_transfer"]
                    product.tag_card_usage = tags["card_usage"]
                    product.tag_housing_subscription = tags["housing_subscription"]
                    product.age_min = tags["age_min"]
                    product.age_max = tags["age_max"]
                    update_fields += _TAG_FIELDS
            if do_summary:
                summary = generate_ai_summary(product)
                if summary is not None:
                    product.ai_summary = summary
                    update_fields.append("ai_summary")

            if update_fields:
                product.save(update_fields=update_fields)
                done += 1

        self.stdout.write(self.style.SUCCESS(f"LLM 보강: 상품 {done}개 갱신"))
