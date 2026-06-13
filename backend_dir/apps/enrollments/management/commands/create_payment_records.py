"""납입 자동기록 배치 (CLAUDE.md 6.2).

매일 오전 cron으로 돌며, 오늘이 이체일인 가입 건에 대해 PaymentRecord를 INSERT한다.
- 기본 가정: 자동이체는 성공(status=PAID, amount=monthly_amount). 사용자가 실제와 다르면 #12로 정정.
- 말일 처리: transfer_day가 그달 일수보다 크면(예: 31일인데 2월) 그달 말일에 기록.
- 만기 이후(enrolled_at + term_months 초과)는 더 이상 기록하지 않음.
- 중복 방지: (enrollment, scheduled_date) UNIQUE + get_or_create로 두 번 INSERT 안 됨.
"""
import calendar
from datetime import date

from django.core.management.base import BaseCommand

from apps.enrollments.models import Enrollment, PaymentRecord
from apps.enrollments.utils import add_months


class Command(BaseCommand):
    help = "오늘이 이체일인 가입 건에 PaymentRecord를 자동 생성한다."

    def handle(self, *args, **options):
        today = date.today()
        # 이번 달 말일(28~31). transfer_day가 이보다 크면 말일로 당겨 비교한다.
        last_day_of_month = calendar.monthrange(today.year, today.month)[1]

        created = 0
        # 이미 가입일이 도래한 건만 대상.
        enrollments = Enrollment.objects.filter(enrolled_at__lte=today)
        for enrollment in enrollments:
            # 1) 오늘이 이 가입의 이체일인가? (말일 보정)
            effective_day = min(enrollment.transfer_day, last_day_of_month)
            if today.day != effective_day:
                continue

            # 2) 만기가 지났으면 더 이상 기록하지 않음.
            maturity = add_months(enrollment.enrolled_at, enrollment.term_months)
            if today > maturity:
                continue

            # 3) (enrollment, 오늘) 레코드 INSERT. 이미 있으면 created=False.
            _, is_created = PaymentRecord.objects.get_or_create(
                enrollment=enrollment,
                scheduled_date=today,
                defaults={
                    "amount": enrollment.monthly_amount,
                    "status": PaymentRecord.Status.PAID,
                    "is_modified": False,
                },
            )
            if is_created:
                created += 1

        self.stdout.write(
            self.style.SUCCESS(f"완료: PaymentRecord {created}건 생성 ({today})")
        )
