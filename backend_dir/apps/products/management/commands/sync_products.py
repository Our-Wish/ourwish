import requests
from django.conf import settings
from django.core.management.base import BaseCommand
from django.db import transaction

from apps.products.models import Bank, Product, ProductOption

FSS_BASE_URL = "http://finlife.fss.or.kr/finlifeapi/savingProductsSearch.json"
# 020000=시중은행(1금융권), 030300=저축은행
TOP_FIN_GRP_NOS = ["020000", "030300"]
GRP_TO_BANK_TYPE = {
    "020000": Bank.BankType.FIRST_TIER,
    "030300": Bank.BankType.SAVINGS,
}


class Command(BaseCommand):
    help = "금감원 API에서 적금 상품을 받아 DB에 적재 (1차: LLM 없이 데이터만)"

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
                        product, _ = Product.objects.update_or_create(
                            bank=bank,
                            fin_prdt_cd=item["fin_prdt_cd"],
                            defaults={
                                "product_name": item["fin_prdt_nm"],
                                "join_member": item.get("join_member") or "",
                                "join_way": item.get("join_way") or "",
                                "max_limit": item.get("max_limit"),
                                "maturity_interest": item.get("mrtr_int") or "",
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
                                "max_rate": opt.get("intr_rate"),
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
