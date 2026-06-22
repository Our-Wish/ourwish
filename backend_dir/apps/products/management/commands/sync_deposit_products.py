from django.conf import settings
from django.core.management.base import BaseCommand

from apps.products.fss_sync import FSSProductSync
from apps.products.models import Product

FSS_BASE_URL = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"


class Command(BaseCommand):
    help = "금감원 API에서 예금 상품을 받아 DB에 적재. --with-llm 시 GMS로 태그·요약 보강"

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

    def handle(self, *args, **options):
        sync = FSSProductSync(
            fss_api_key=settings.FSS_API_KEY,
            base_url=FSS_BASE_URL,
            product_type=Product.ProductType.DEPOSIT,
            # 예금(거치식)은 FSS optionList에 적립유형(rsrv_type) 필드가 없음.
            has_rsrv_type=False,
        )
        total_products, total_options = sync.run(self.stdout, self.stderr)
        self.stdout.write(
            self.style.SUCCESS(
                f"완료: 상품 {total_products}개, 옵션 {total_options}개 적재"
            )
        )

        if options["with_llm"]:
            sync.enrich_with_llm(
                self.stdout, limit=options["llm_limit"], only=options["llm_only"]
            )
