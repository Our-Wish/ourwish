from django.urls import path

from .views import (
    EnrollmentDeleteView,
    EnrollmentListCreateView,
    PaymentRecordUpdateView,
)

urlpatterns = [
    # GET(목록) + POST(가입)
    path("", EnrollmentListCreateView.as_view(), name="enrollment_list_create"),
    # DELETE(삭제)
    path(
        "<int:enrollment_id>/",
        EnrollmentDeleteView.as_view(),
        name="enrollment_delete",
    ),
    # PATCH(납입 정정)
    path(
        "<int:enrollment_id>/payments/<int:record_id>/",
        PaymentRecordUpdateView.as_view(),
        name="payment_update",
    ),
]
