from django.urls import path

from .views import SignupView, LoginView, CheckIdView, TokenRefreshView, MemberGoalAmountView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("check-id/", CheckIdView.as_view(), name="check_id"),
    path("me/", MemberGoalAmountView.as_view(), name="member_me"),
]
