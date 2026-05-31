from django.db import models
from apps.accounts.models import Member


# Create your models here.
class Goal(models.Model):
    member = models.ForeignKey(Member, on_delete=models.CASCADE, related_name="goals")
    term_months = models.IntegerField()
    monthly_cap = models.IntegerField()
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "goal"
