from django.db.models import Count
from drf_spectacular.utils import extend_schema
from rest_framework import status
from rest_framework.exceptions import NotFound, PermissionDenied
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView

from .models import Comment, Post
from .serializers import (
    CommentSerializer,
    CommentWriteSerializer,
    PostDetailSerializer,
    PostListSerializer,
    PostWriteSerializer,
)


class PostListCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        responses=PostListSerializer(many=True),
        summary="커뮤니티 글 목록",
    )
    def get(self, request):
        # 작성자는 한 번에 join(select_related), 댓글 수는 집계(annotate)로 N+1 방지.
        posts = (
            Post.objects.select_related("author")
            .annotate(comment_count=Count("comments"))
            .order_by("-created_at")
        )
        return Response(PostListSerializer(posts, many=True).data)

    @extend_schema(
        request=PostWriteSerializer,
        responses={201: PostDetailSerializer},
        summary="커뮤니티 글 작성",
    )
    def post(self, request):
        serializer = PostWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        # 작성자는 요청 본문이 아니라 로그인한 사용자로 강제한다(위조 방지).
        post = serializer.save(author=request.user)
        return Response(
            PostDetailSerializer(post).data,
            status=status.HTTP_201_CREATED,
        )


class PostDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_post(self, post_id):
        # 상세/댓글까지 한 번에 끌어오도록 prefetch.
        try:
            return (
                Post.objects.select_related("author")
                .prefetch_related("comments__author")
                .get(id=post_id)
            )
        except Post.DoesNotExist:
            raise NotFound("해당 글을 찾을 수 없습니다.")

    def _check_owner(self, post, request):
        if post.author_id != request.user.id:
            raise PermissionDenied("본인이 작성한 글만 수정/삭제할 수 있습니다.")

    @extend_schema(responses=PostDetailSerializer, summary="커뮤니티 글 상세")
    def get(self, request, post_id):
        post = self._get_post(post_id)
        return Response(PostDetailSerializer(post).data)

    @extend_schema(
        request=PostWriteSerializer,
        responses={200: PostDetailSerializer},
        summary="커뮤니티 글 수정 (작성자만)",
    )
    def patch(self, request, post_id):
        post = self._get_post(post_id)
        self._check_owner(post, request)
        # 일부 필드만 보내도 되도록 partial=True.
        serializer = PostWriteSerializer(post, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(PostDetailSerializer(post).data)

    @extend_schema(responses={204: None}, summary="커뮤니티 글 삭제 (작성자만)")
    def delete(self, request, post_id):
        post = self._get_post(post_id)
        self._check_owner(post, request)
        post.delete()  # 댓글은 FK on_delete=CASCADE로 함께 삭제됨.
        return Response(status=status.HTTP_204_NO_CONTENT)


class CommentCreateView(APIView):
    permission_classes = [IsAuthenticated]

    @extend_schema(
        request=CommentWriteSerializer,
        responses={201: CommentSerializer},
        summary="댓글 작성",
    )
    def post(self, request, post_id):
        # 댓글을 달 글이 실제로 있는지 먼저 확인.
        if not Post.objects.filter(id=post_id).exists():
            raise NotFound("해당 글을 찾을 수 없습니다.")
        serializer = CommentWriteSerializer(data=request.data)
        serializer.is_valid(raise_exception=True)
        comment = serializer.save(author=request.user, post_id=post_id)
        return Response(
            CommentSerializer(comment).data,
            status=status.HTTP_201_CREATED,
        )


class CommentDetailView(APIView):
    permission_classes = [IsAuthenticated]

    def _get_owned(self, comment_id, request):
        try:
            comment = Comment.objects.select_related("author").get(id=comment_id)
        except Comment.DoesNotExist:
            raise NotFound("해당 댓글을 찾을 수 없습니다.")
        if comment.author_id != request.user.id:
            raise PermissionDenied("본인이 작성한 댓글만 수정/삭제할 수 있습니다.")
        return comment

    @extend_schema(
        request=CommentWriteSerializer,
        responses={200: CommentSerializer},
        summary="댓글 수정 (작성자만)",
    )
    def patch(self, request, comment_id):
        comment = self._get_owned(comment_id, request)
        serializer = CommentWriteSerializer(comment, data=request.data, partial=True)
        serializer.is_valid(raise_exception=True)
        serializer.save()
        return Response(CommentSerializer(comment).data)

    @extend_schema(responses={204: None}, summary="댓글 삭제 (작성자만)")
    def delete(self, request, comment_id):
        comment = self._get_owned(comment_id, request)
        comment.delete()
        return Response(status=status.HTTP_204_NO_CONTENT)
