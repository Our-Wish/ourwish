from django.urls import path

from .views import (
    SignupView,
    LoginView,
    CheckIdView,
    TokenRefreshView,
    MemberMeView,
)

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("check-id/", CheckIdView.as_view(), name="check_id"),
    # GET(내 정보) + PATCH(닉네임 수정)
    path("me/", MemberMeView.as_view(), name="member_me"),
]
