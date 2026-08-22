from django.conf import settings
from django.core.management.base import BaseCommand

from apps.products.fss_sync import FSSProductSync
from apps.products.models import Product

FSS_BASE_URL = "http://finlife.fss.or.kr/finlifeapi/depositProductsSearch.json"


class Command(BaseCommand):
    help = "금감원 API에서 예금 상품을 받아 DB에 적재"

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
