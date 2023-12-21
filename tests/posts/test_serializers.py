import pytest
from posts.serializers import PostSerializer
from tests.factories import PostFactory, UserFactory
from django.test import TestCase

pytestmark = pytest.mark.django_db

class TestPostSerializer(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.post = PostFactory()


    def test_update_post(self):
        serializer = PostSerializer(instance=self.post,
                                    data={'title': 'Updated Title',
                                            'content': 'Updated Content', 'read_permission': 'public', 'edit_permission': 'public',
                                            'author': self.user.id,
                                            })
        assert serializer.is_valid()
        updated_post = serializer.save()
        assert updated_post.title == 'Updated Title'
        assert updated_post.content == 'Updated Content'
        assert updated_post.read_permission == 'public'
        assert updated_post.edit_permission == 'public'
        
    def test_update_post_missing_title(self):
        serializer = PostSerializer(instance=self.post,
                                    data={'content': 'Updated Content', 'read_permission': 'public', 'edit_permission': 'public',
                                    'author': self.user.id,
                                    })
        assert not serializer.is_valid()
        assert 'title' in serializer.errors
        
    def test_update_post_missing_content(self):
        serializer = PostSerializer(instance=self.post,
                                    data={'title': 'Updated Title', 
                                          'read_permission': 'public', 'edit_permission': 'public',
                                            'author': self.user.id,
                                    })
        assert not serializer.is_valid()
        assert 'content' in serializer.errors
        