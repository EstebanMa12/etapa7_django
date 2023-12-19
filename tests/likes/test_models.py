import pytest

from tests.factories import PostFactory, UserFactory
from django.db.utils import IntegrityError

pytestmark = pytest.mark.django_db


class TestLikeModel:

    @pytest.mark.django_db
    def test_create_like(self, likes_factory):
        post = PostFactory()
        user = UserFactory()
        like = likes_factory(post=post, user=user)
        assert like.post is not None
        assert like.user is not None
        assert like.post == post
        assert like.user == user
        assert like.__str__() == post.title + ' - ' + user.username
        
    @pytest.mark.django_db
    def test_create_like_missing_post(self, likes_factory):
        user = UserFactory()
        with pytest.raises(IntegrityError) as e:
            likes_factory(post=None,user=user)
        assert str(e.value) == 'NOT NULL constraint failed: likes_like.post_id'

    @pytest.mark.django_db
    def test_create_like_missing_user(self, likes_factory):
        post = PostFactory()
        with pytest.raises(IntegrityError) as e:
            likes_factory(post=post,user=None)
        assert str(e.value) == 'NOT NULL constraint failed: likes_like.user_id'
            