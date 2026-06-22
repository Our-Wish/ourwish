from rest_framework import serializers

from .models import Comment, Post


class CommentSerializer(serializers.ModelSerializer):
    """댓글 한 줄(읽기용). 작성자는 닉네임만 노출한다."""

    author_id = serializers.IntegerField(source="author.id", read_only=True)
    author_nickname = serializers.CharField(source="author.nickname", read_only=True)

    class Meta:
        model = Comment
        fields = [
            "id",
            "author_id",
            "author_nickname",
            "content",
            "created_at",
            "updated_at",
        ]


class CommentWriteSerializer(serializers.ModelSerializer):
    """댓글 작성·수정 요청 — content만 받는다(작성자·글은 뷰에서 채운다)."""

    class Meta:
        model = Comment
        fields = ["content"]

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("댓글 내용을 입력해 주세요.")
        return value


class PostListSerializer(serializers.ModelSerializer):
    """글 목록 한 줄 — 본문 대신 작성자·댓글 수만 보여준다."""

    author_id = serializers.IntegerField(source="author.id", read_only=True)
    author_nickname = serializers.CharField(source="author.nickname", read_only=True)
    comment_count = serializers.IntegerField(read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "author_id",
            "author_nickname",
            "comment_count",
            "created_at",
        ]


class PostDetailSerializer(serializers.ModelSerializer):
    """글 상세 — 본문 + 달린 댓글 전체를 함께 내려준다."""

    author_id = serializers.IntegerField(source="author.id", read_only=True)
    author_nickname = serializers.CharField(source="author.nickname", read_only=True)
    comments = CommentSerializer(many=True, read_only=True)

    class Meta:
        model = Post
        fields = [
            "id",
            "title",
            "content",
            "author_id",
            "author_nickname",
            "comments",
            "created_at",
            "updated_at",
        ]


class PostWriteSerializer(serializers.ModelSerializer):
    """글 작성·수정 요청 — 제목·본문만 받는다(작성자는 뷰에서 채운다)."""

    class Meta:
        model = Post
        fields = ["title", "content"]

    def validate_title(self, value):
        if not value.strip():
            raise serializers.ValidationError("제목을 입력해 주세요.")
        return value

    def validate_content(self, value):
        if not value.strip():
            raise serializers.ValidationError("내용을 입력해 주세요.")
        return value
