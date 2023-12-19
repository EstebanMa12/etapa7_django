
import pytest
from likes.serializers import LikeSerializer
from tests.factories import PostFactory, UserFactory
pytestmark = pytest.mark.django_db

class TestLikeSerializer:

    def test_create_like(self):
        post = PostFactory()
        user = UserFactory()
        serializer = LikeSerializer(data={'post': post.id, 'user': user.id})
        assert serializer.is_valid()
        like = serializer.save()
        assert like.post == post
        assert like.user == user

    def test_create_like_missing_post(self):
        user = UserFactory()
        serializer = LikeSerializer(data={'user': user.id})
        assert not serializer.is_valid()
        assert 'post' in serializer.errors

    def test_create_like_missing_user(self):
        post = PostFactory()
        serializer = LikeSerializer(data={'post': post.id})
        assert not serializer.is_valid()
        assert 'user' in serializer.errors

    def test_create_like_invalid_post(self):
        user = UserFactory()
        serializer = LikeSerializer(data={'post': 100, 'user': user.id})
        assert not serializer.is_valid()
        assert 'post' in serializer.errors

    def test_create_like_invalid_user(self):
        post = PostFactory()
        serializer = LikeSerializer(data={'post': post.id, 'user': 100})
        assert not serializer.is_valid()
        assert 'user' in serializer.errors

    def test_create_like_missing_all_fields(self):
        serializer = LikeSerializer(data={})
        assert not serializer.is_valid()
        assert 'post' in serializer.errors
        assert 'user' in serializer.errors