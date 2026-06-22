"""금감원(FSS) 적금/예금 공통 동기화 로직.

적금(savingProductsSearch.json)과 예금(depositProductsSearch.json)은
baseList 필드가 동일하고, optionList은 예금에 적립유형(rsrv_type/rsrv_type_nm)이
없다는 점만 다르다. 그래서 두 management command(sync_products,
sync_deposit_products)가 이 모듈의 FSSProductSync를 product_type/has_rsrv_type만
다르게 줘서 공유한다.
"""
import requests
from django.db import transaction

from apps.products.llm import generate_ai_summary, generate_tags
from apps.products.models import Bank, Product, ProductOption

# 020000=시중은행(1금융권), 030300=저축은행 — 적금/예금 공통.
TOP_FIN_GRP_NOS = ["020000", "030300"]
GRP_TO_BANK_TYPE = {
    "020000": Bank.BankType.FIRST_TIER,
    "030300": Bank.BankType.SAVINGS,
}

# LLM이 채우는 태그·연령 필드(ai_summary는 루프에서 별도로 처리).
TAG_FIELDS = [
    "tag_salary_transfer",
    "tag_auto_transfer",
    "tag_card_usage",
    "tag_housing_subscription",
    "age_min",
    "age_max",
]


class FSSProductSync:
    """FSS API 호출 → Bank/Product/ProductOption 적재 + (옵션) LLM 보강.

    base_url: FSS 검색 API URL(적금/예금 각각 다름).
    product_type: Product.ProductType.SAVINGS 또는 DEPOSIT.
    has_rsrv_type: optionList에 적립유형(rsrv_type) 필드가 있는지(적금=True, 예금=False).
    """

    def __init__(self, fss_api_key, base_url, product_type, has_rsrv_type):
        self.fss_api_key = fss_api_key
        self.base_url = base_url
        self.product_type = product_type
        self.has_rsrv_type = has_rsrv_type

    def _fetch(self, grp_no, page_no):
        res = requests.get(
            self.base_url,
            params={
                "auth": self.fss_api_key,
                "topFinGrpNo": grp_no,
                "pageNo": page_no,
            },
            timeout=30,
        )
        return res.json()["result"]

    def run(self, stdout, stderr):
        """동기화 실행. (총 상품 수, 총 옵션 수) 반환."""
        total_products = 0
        total_options = 0

        with transaction.atomic():
            for grp_no in TOP_FIN_GRP_NOS:
                bank_type = GRP_TO_BANK_TYPE[grp_no]
                page_no = 1
                while True:
                    data = self._fetch(grp_no, page_no)
                    if data.get("err_cd") != "000":
                        stderr.write(f"[{grp_no}] API 오류: {data.get('err_msg')}")
                        break

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
                                "product_type": self.product_type,
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

                    for opt in data.get("optionList", []):
                        product = product_map.get(
                            (opt["fin_co_no"], opt["fin_prdt_cd"])
                        )
                        if product is None or opt.get("intr_rate") is None:
                            continue
                        rsrv_type = opt["rsrv_type"] if self.has_rsrv_type else None
                        ProductOption.objects.update_or_create(
                            product=product,
                            save_term=opt["save_trm"],
                            intr_rate_type=opt["intr_rate_type"],
                            rsrv_type=rsrv_type,
                            defaults={
                                "base_rate": opt["intr_rate"],
                                "max_rate": opt.get("intr_rate2"),
                            },
                        )
                        total_options += 1

                    if page_no >= data.get("max_page_no", 1):
                        break
                    page_no += 1

        return total_products, total_options

    def enrich_with_llm(self, stdout, limit=0, only=None):
        """아직 LLM 처리 안 된(ai_summary가 NULL인) 이 product_type 상품을 GMS로 채운다.

        only=None이면 태그+요약 둘 다, "tags"면 태그·연령만, "summary"면 AI요약만.
        """
        do_tags = only in (None, "tags")
        do_summary = only in (None, "summary")

        products = Product.objects.filter(
            product_type=self.product_type, ai_summary__isnull=True
        )
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
                    update_fields += TAG_FIELDS
            if do_summary:
                summary = generate_ai_summary(product)
                if summary is not None:
                    product.ai_summary = summary
                    update_fields.append("ai_summary")

            if update_fields:
                product.save(update_fields=update_fields)
                done += 1

        stdout.write(f"LLM 보강: 상품 {done}개 갱신")
        return done
