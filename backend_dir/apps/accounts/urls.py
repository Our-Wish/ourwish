from django.urls import path

from .views import SignupView, LoginView, CheckIdView, TokenRefreshView

urlpatterns = [
    path("signup/", SignupView.as_view(), name="signup"),
    path("login/", LoginView.as_view(), name="login"),
    path("token/refresh/", TokenRefreshView.as_view(), name="token_refresh"),
    path("check-id/", CheckIdView.as_view(), name="check_id"),
]
