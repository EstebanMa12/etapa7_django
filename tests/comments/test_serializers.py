import pytest

from django.db.utils import IntegrityError
from django.contrib.auth import get_user_model

from comments.models import Comment
from comments.serializers import CommentSerializer
from tests.factories import PostFactory, UserFactory

User = get_user_model()

pytestmark = pytest.mark.django_db


class TestCommentSerializer:

    def test_create_comment(self):
        post = PostFactory()
        user = UserFactory()
        serializer = CommentSerializer(data={'post': post.id, 'user': user.id, 'content': 'Test Comment'})
        assert serializer.is_valid()
        comment = serializer.save()
        assert comment.post == post
        assert comment.user == user
        assert comment.content == 'Test Comment'

    def test_create_comment_missing_post(self):
        user = UserFactory()
        serializer = CommentSerializer(data={'user': user.id, 'content': 'Test Comment'})
        assert not serializer.is_valid()
        assert 'post' in serializer.errors

    def test_create_comment_missing_user(self):
        post = PostFactory()
        serializer = CommentSerializer(data={'post': post.id, 'content': 'Test Comment'})
        assert not serializer.is_valid()
        assert 'user' in serializer.errors

    def test_create_comment_missing_content(self):
        post = PostFactory()
        user = UserFactory()
        serializer = CommentSerializer(data={'post': post.id, 'user': user.id})
        assert not serializer.is_valid()
        assert 'content' in serializer.errors
    
    def test_create_comment_invalid_post(self):
        user = UserFactory()
        serializer = CommentSerializer(data={'post': 100, 'user': user.id, 'content': 'Test Comment'})
        assert not serializer.is_valid()
        assert 'post' in serializer.errors
    
    def test_create_comment_invalid_user(self):
        post = PostFactory()
        serializer = CommentSerializer(data={'post': post.id, 'user': 100, 'content': 'Test Comment'})
        assert not serializer.is_valid()
        assert 'user' in serializer.errors
    
    def test_create_comment_invalid_content(self):
        post = PostFactory()
        user = UserFactory()
        serializer = CommentSerializer(data={'post': post.id, 'user': user.id, 'content': ''})
        assert not serializer.is_valid()
        assert 'content' in serializer.errors
    
    def test_create_comment_invalid_content_length(self):
        post = PostFactory()
        user = UserFactory()
        serializer = CommentSerializer(data={'post': post.id, 'user': user.id, 'content': 'a'*1001})
        assert not serializer.is_valid()
        assert 'content' in serializer.errors
    
    def test_create_comment_missing_all_fields(self):
        serializer = CommentSerializer(data={})
        assert not serializer.is_valid()
        assert 'post' in serializer.errors
        assert 'user' in serializer.errors
        assert 'content' in serializer.errors
    