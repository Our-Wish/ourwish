from django.urls import path

from .views import EnrollmentCreateView

urlpatterns = [
    path("", EnrollmentCreateView.as_view(), name="enrollment_create"),
]
