from django.urls import path

from .views import (
    CommentCreateView,
    CommentDetailView,
    PostDetailView,
    PostListCreateView,
)

urlpatterns = [
    # GET(목록) + POST(글 작성)
    path("posts/", PostListCreateView.as_view(), name="post_list_create"),
    # GET(상세) + PATCH(수정) + DELETE(삭제)
    path("posts/<int:post_id>/", PostDetailView.as_view(), name="post_detail"),
    # POST(댓글 작성) — 어느 글에 다는지 post_id로 식별
    path(
        "posts/<int:post_id>/comments/",
        CommentCreateView.as_view(),
        name="comment_create",
    ),
    # PATCH(댓글 수정) + DELETE(댓글 삭제) — comment_id로 식별
    path(
        "comments/<int:comment_id>/",
        CommentDetailView.as_view(),
        name="comment_detail",
    ),
]
