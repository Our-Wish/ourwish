"""기존 상품에 min_limit(+예금은 태그)을 LLM으로 재추출해 채우는 일회성 백필.

- 적금(SAVINGS): AI요약·태그는 이미 있으므로 min_limit만 채운다.
- 예금(DEPOSIT): 새 태그(첫거래·비대면·마케팅·재예치) + min_limit을 채운다(AI요약은 나중에).
- AI요약(ai_summary)은 어느 경우에도 건드리지 않는다(GMS 호출·비용 절약).

사용 예:
  # 로컬에서 예금 5개만 저장 없이 확인
  python manage.py retag_products --type DEPOSIT --limit 5 --dry-run
  # 서버에서 실제 적재
  python manage.py retag_products --type SAVINGS
  python manage.py retag_products --type DEPOSIT
"""
from django.core.management.base import BaseCommand

from apps.products.llm import generate_tags
from apps.products.models import Product

# 예금에 저장할 태그 컬럼 ← generate_tags 결과 키.
_DEPOSIT_TAG_COLUMNS = {
    "tag_first_transaction": "first_transaction",
    "tag_online_signup": "online_signup",
    "tag_marketing_consent": "marketing_consent",
    "tag_redeposit": "redeposit",
}


class Command(BaseCommand):
    help = "기존 상품에 min_limit(+예금은 태그)을 LLM으로 재추출해 채운다(요약은 미변경)."

    def add_arguments(self, parser):
        parser.add_argument(
            "--type",
            choices=["SAVINGS", "DEPOSIT"],
            help="상품군 한정(미지정=전체)",
        )
        parser.add_argument(
            "--limit", type=int, default=0, help="처리할 최대 개수(0=전부)"
        )
        parser.add_argument(
            "--dry-run",
            action="store_true",
            help="저장하지 않고 추출 결과만 출력(로컬 확인용)",
        )

    def handle(self, *args, **opts):
        qs = Product.objects.all().order_by("id")
        if opts["type"]:
            qs = qs.filter(product_type=opts["type"])
        if opts["limit"]:
            qs = qs[: opts["limit"]]

        saved = 0
        failed = 0
        for product in qs:
            tags = generate_tags(product)
            if not tags:
                failed += 1
                self.stderr.write(f"  ! [{product.id}] {product.product_name}: LLM 빈 응답 — 건너뜀")
                continue

            # 모든 상품: min_limit 채움.
            fields = ["min_limit"]
            product.min_limit = tags["min_limit"]
            # 예금만: 새 태그까지 채움.
            if product.product_type == Product.ProductType.DEPOSIT:
                for column, key in _DEPOSIT_TAG_COLUMNS.items():
                    setattr(product, column, tags[key])
                fields += list(_DEPOSIT_TAG_COLUMNS)

            shown = {f: getattr(product, f) for f in fields}
            self.stdout.write(f"  [{product.id}] {product.product_type} {product.product_name}: {shown}")

            if not opts["dry_run"]:
                product.save(update_fields=fields)
                saved += 1

        if opts["dry_run"]:
            self.stdout.write(self.style.SUCCESS(f"DRY-RUN 완료 — 저장 안 함 (실패 {failed}개)"))
        else:
            self.stdout.write(self.style.SUCCESS(f"완료 — {saved}개 저장 (실패 {failed}개)"))
