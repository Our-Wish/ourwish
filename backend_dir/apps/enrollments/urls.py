from django.urls import path

from .views import EnrollmentDetailView, EnrollmentListCreateView

urlpatterns = [
    # GET(목록) + POST(상품 등록)
    path("", EnrollmentListCreateView.as_view(), name="enrollment_list_create"),
    # PATCH(정보 입력/수정) + DELETE(삭제)
    path(
        "<int:enrollment_id>/",
        EnrollmentDetailView.as_view(),
        name="enrollment_detail",
    ),
]
