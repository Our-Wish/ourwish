from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from apps.products.models import Product
from .models import Enrollment
from .serializers import (
    EnrollmentInfoSerializer,
    EnrollmentListSerializer,
    EnrollmentRegisterSerializer,
)


class EnrollmentListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=EnrollmentListSerializer(many=True),
        summary="나의 상품 관리 목록 (#10)",
    )
    def get(self, request):
        enrollments = (
            Enrollment.objects.filter(member=request.user)
            .select_related("product", "product__bank")
            .order_by("-created_at")
        )
        return Response(EnrollmentListSerializer(enrollments, many=True).data)

    @extend_schema(
        request=EnrollmentRegisterSerializer,
        responses={201: EnrollmentListSerializer},
        summary="상품 등록 (#9, 1단계: 상품만 등록)",
    )
    def post(self, request):
        serializer = EnrollmentRegisterSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)

        try:
            product = Product.objects.select_related("bank").get(
                id=serializer.validated_data["product_id"]
            )
        except Product.DoesNotExist:
            raise NotFound("해당 상품을 찾을 수 없습니다.")

        if Enrollment.objects.filter(member=request.user, product=product).exists():
            return Response(
                {"detail": "이미 등록한 상품입니다."},
                status=status.HTTP_409_CONFLICT,
            )

        enrollment = Enrollment.objects.create(member=request.user, product=product)
        return Response(
            EnrollmentListSerializer(enrollment).data,
            status=status.HTTP_201_CREATED,
        )


class EnrollmentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_owned(self, request, enrollment_id):
        # id로 먼저 찾고(없으면 404), 소유자 확인(아니면 403).
        try:
            enrollment = Enrollment.objects.select_related(
                "product", "product__bank"
            ).get(id=enrollment_id)
        except Enrollment.DoesNotExist:
            raise NotFound("해당 가입 내역을 찾을 수 없습니다.")
        if enrollment.member_id != request.user.id:
            raise PermissionDenied("본인의 가입 내역만 다룰 수 있습니다.")
        return enrollment

    @extend_schema(
        request=EnrollmentInfoSerializer,
        responses={200: EnrollmentListSerializer},
        summary="가입 정보 입력/수정 (2단계)",
    )
    def patch(self, request, enrollment_id):
        enrollment = self._get_owned(request, enrollment_id)
        serializer = EnrollmentInfoSerializer(enrollment, data=request.data)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(EnrollmentListSerializer(enrollment).data)

    @extend_schema(responses={204: None}, summary="가입 상품 삭제 (#11)")
    def delete(self, request, enrollment_id):
        enrollment = self._get_owned(request, enrollment_id)
        enrollment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
