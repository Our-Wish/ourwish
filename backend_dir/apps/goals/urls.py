from django.urls import path

from .views import GoalCreateView, GoalLatestView

urlpatterns = [
    path("", GoalCreateView.as_view(), name="goal_create"),
    path("latest/", GoalLatestView.as_view(), name="goal_latest"),
]
