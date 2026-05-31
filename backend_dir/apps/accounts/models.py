from django.db import models


# Create your models here.
class Member(models.Model):
    class JobStatus(models.TextChoices):
        STUDENT = "STUDENT", "학생"
        EMPLOYED = "EMPLOYED", "직장인"
        OTHER = "OTHER", "기타"

    class MaritalStatus(models.TextChoices):
        SINGLE = "SINGLE", "미혼"
        MARRIED = "MARRIED", "기혼"

    login_id = models.CharField(max_length=50, unique=True)
    password_hash = models.CharField(max_length=128)
    nickname = models.CharField(max_length=50)
    birth_date = models.DateField()
    job_status = models.CharField(max_length=10, choices=JobStatus.choices)
    marital_status = models.CharField(max_length=10, choices=MaritalStatus.choices)
    total_goal_amount = models.BigIntegerField(null=True, blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    class Meta:
        db_table = "member"
