import pytest
pytestmark = pytest.mark.django_db
from tests.factories import PostFactory, UserFactory
from django.core.exceptions import ValidationError
from django.db.utils import IntegrityError

class TestCommentModel:
        @pytest.mark.django_db
        def test_create_comment(self, comments_factory):
            post = PostFactory()
            user = UserFactory()
            content = "Test content"
            comment = comments_factory(post=post, user=user, content = content)
            assert comment.post is not None
            assert comment.user is not None
            assert comment.post == post
            assert comment.user == user
            
        @pytest.mark.django_db
        def test_create_comment_missing_post(self, comments_factory):
            user = UserFactory()
            content = "Test content"
            with pytest.raises(IntegrityError) as e:
                comments_factory(post=None, user=user, content=content)
            assert str(e.value) == 'NOT NULL constraint failed: comments_comment.post_id'
                
        @pytest.mark.django_db
        def test_create_comment_missing_user(self, comments_factory):
            post = PostFactory()
            content = "Test content"
            with pytest.raises(IntegrityError) as e:
                comments_factory(post=post, user=None, content=content)
            assert str(e.value) == 'NOT NULL constraint failed: comments_comment.user_id'
                
        @pytest.mark.django_db
        def test_create_comment_missing_content(self, comments_factory):
            post = PostFactory()
            user = UserFactory()
            content = ""
            try:
                comments_factory(post=post, user=user, content = content)
            except ValueError as e:
                assert str(e) == 'Comments must have content'
        
        @pytest.mark.django_db
        def test_comment_str(self, comments_factory):
            post = PostFactory()
            user = UserFactory()
            content = "Test content"
            comment = comments_factory(post=post, user=user, content = content)
            assert comment.__str__() == post.title + ' - ' + user.username + ' - ' + comment.content[:20]
