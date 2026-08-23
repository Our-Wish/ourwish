"""가입 상품 금액 단위 정리.

예전 프론트가 '만원' 입력값(예: 50)을 그대로 보내 원 단위 컬럼에 만원 값이 저장돼 있었다.
프론트 최소 입력이 5만원이라 실제 원 단위 값은 항상 10,000 이상이므로,
10,000 미만인 값은 만원 단위로 보고 10,000을 곱해 원으로 맞춘다.
"""
from django.db import migrations


def won_from_manwon(apps, schema_editor):
    Enrollment = apps.get_model("enrollments", "Enrollment")
    for e in Enrollment.objects.all():
        fields = []
        if e.monthly_amount is not None and e.monthly_amount < 10_000:
            e.monthly_amount *= 10_000
            fields.append("monthly_amount")
        if e.deposit_amount is not None and e.deposit_amount < 10_000:
            e.deposit_amount *= 10_000
            fields.append("deposit_amount")
        if fields:
            e.save(update_fields=fields)


class Migration(migrations.Migration):

    dependencies = [
        ("enrollments", "0003_enrollment_deposit_amount"),
    ]

    operations = [
        migrations.RunPython(won_from_manwon, migrations.RunPython.noop),
    ]
