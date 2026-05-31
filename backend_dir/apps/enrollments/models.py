from django.db import models
from apps.accounts.models import Member
from apps.products.models import Product


# Create your models here.
class Enrollment(models.Model):
    member = models.ForeignKey(
        Member, on_delete=models.CASCADE, related_name="enrollments"
    )
    product = models.ForeignKey(
        Product, on_delete=models.RESTRICT, related_name="enrollments"
    )
    monthly_amount = models.IntegerField()
    term_months = models.IntegerField()
    expected_payout_at_maturity = models.BigIntegerField()
    calculated_at = models.DateTimeField(auto_now_add=True)
    transfer_day = models.IntegerField()
    enrolled_at = models.DateField()

    class Meta:
        db_table = "enrollment"
        unique_together = [("member", "product")]


class PaymentRecord(models.Model):
    class Status(models.TextChoices):
        PAID = "PAID", "납입"
        MISSED = "MISSED", "미납"
        PARTIAL = "PARTIAL", "부분납입"

    enrollment = models.ForeignKey(
        Enrollment, on_delete=models.CASCADE, related_name="payment_records"
    )
    scheduled_date = models.DateField()
    amount = models.IntegerField()
    status = models.CharField(max_length=10, choices=Status.choices)
    is_modified = models.BooleanField(default=False)
    recorded_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "payment_record"
        unique_together = [("enrollment", "scheduled_date")]
