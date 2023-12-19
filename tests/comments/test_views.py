import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from tests.factories import  PostFactory, UserFactory
from django.test import TestCase
pytestmark = pytest.mark.django_db

class TestCommentCreateView(TestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.post = PostFactory()

    def test_create_comment_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
        data = {'content': 'This is a test comment'}
        response = self.client.post(url, data)

        assert response.status_code == status.HTTP_200_OK
        assert 'message' in response.data
        

    def test_create_comment_as_unauthenticated_user(self):

        url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
        data = {'content': 'This is a test comment'}
        response = self.client.post(url, data)

        assert response.status_code == status.HTTP_403_FORBIDDEN
    
    def test_delete_comment_as_authenticated_user(self):
        if self.post.read_permission == 'public':
            url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
            response = self.client.delete(url)

            assert response.status_code == status.HTTP_200_OK
            assert 'message' in response.data
        else:
            # Sino es public manda un bad REQUEST
            url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
            response = self.client.delete(url)
            assert response.status_code == status.HTTP_403_FORBIDDEN


    # def test_create_comment_with_existing_comment(self):
    #     user = UserFactory()
    #     client = APIClient()
    #     client.force_authenticate(user=user)

    #     post = PostFactory()
    #     CommentsFactory(user=user, post=post)

    #     url = reverse('comment-create', kwargs={'post_id': post.id})
    #     data = {'content': 'This is a test comment'}
    #     response = client.post(url, data)

    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert 'error' in response.data

    # def test_delete_comment_as_authenticated_user(self):
    #     user = UserFactory()
    #     client = APIClient()
    #     client.force_authenticate(user=user)

    #     post = PostFactory()
    #     comment = CommentsFactory(user=user, post=post)

    #     url = reverse('comment-delete', kwargs={'post_id': post.id})
    #     response = client.delete(url)

    #     assert response.status_code == status.HTTP_200_OK
    #     assert 'message' in response.data

    # def test_delete_comment_as_unauthenticated_user(self):
    #     client = APIClient()

    #     post = PostFactory()
    #     comment = CommentsFactory(post=post)

    #     url = reverse('comment-delete', kwargs={'post_id': post.id})
    #     response = client.delete(url)

    #     assert response.status_code == status.HTTP_401_UNAUTHORIZED

    # def test_delete_comment_with_no_existing_comment(self):
    #     user = UserFactory()
    #     client = APIClient()
    #     client.force_authenticate(user=user)

    #     post = PostFactory()

    #     url = reverse('comment-delete', kwargs={'post_id': post.id})
    #     response = client.delete(url)

    #     assert response.status_code == status.HTTP_400_BAD_REQUEST
    #     assert 'error' in response.data
    
    
    # @pytest.mark.parametrize("field", ['content'])
    # def test_create_comment_missing_fields(self, field):
    #     self.client.force_authenticate(user=self.user)
    #     url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
    #     data = {'content': 'This is a test comment'}
    #     data.pop(field)
    #     response = self.client.post(url, data)

    #     assert response.status_code == status.HTTP_200_OK
    #     assert field in response.data
            