import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase, force_authenticate
from tests.factories import  PostFactory, UserFactory
from django.test import TestCase
from comments.models import Comment
pytestmark = pytest.mark.django_db

class TestCommentCreateView(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.post = PostFactory(read_permission='public', edit_permission='public')

    def test_create_comment_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
        data = {'content': 'This is a test comment'}
        
        # Realizar la solicitud
        response = self.client.post(url, data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert 'message' in response.data
        

    def test_create_comment_as_unauthenticated_user(self):
        url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
        data = {'content': 'This is a test comment'}
        
        # Realizar la solicitud
        response = self.client.post(url, data)
        print(response.data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")
        self.assertFalse(Comment.objects.exists(), "No comment should be created for unauthenticated user.")
        
        
        #User is admin
        #User is not autenthicated
            # - Non authenticated users cannot comment on a post regardless of permissions
        #User is autenthicated
        #User is a member of a owner's team
        #Users can delete a comment that they have previously posted
            # - Must have view access to the post
    
    def test_create_comment_as_authenticated_user_with_no_permissions(self):
        self.client = APIClient()
        force_authenticate(self.client,user=self.user)
        self.post.read_permission = 'team'
        self.post.edit_permission = 'team'
        self.post.author.team = 'Another team'
        self.post.author.save()
        self.post.save()
        url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
        data = {'content': 'This is a test comment'}
        
        # Realizar la solicitud
        response = self.client.post(url, data)
        
        print(response.data)
        print(self.user.is_authenticated)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")
        self.assertFalse(Comment.objects.exists(), "No comment should be created for unauthenticated user.")
        
    def test_create_comment_as_authenticated_user_with_read_permissions(self):
        self.client = APIClient()
        force_authenticate(self.client,user=self.user)
        self.post.read_permission = 'authenticated'
        self.post.edit_permission = 'authenticated'
        self.post.save()
        url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
        data = {'content': 'This is a test comment'}
        
        # Realizar la solicitud
        response = self.client.post(url, data)
        
        print(self.user.is_authenticated)
        print(response.data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Comment.objects.exists(), "No comment should be created for unauthenticated user.")

    def test_delete_comment_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
        data = {'content': 'This is a test comment'}
        
        # Realizar la solicitud
        response = self.client.delete(url, data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        assert 'message' in response.data
        
    def test_delete_comment_as_unauthenticated_user(self):
        url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
        data = {'content': 'This is a test comment'}
        
        # Realizar la solicitud
        response = self.client.delete(url, data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")
        self.assertFalse(Comment.objects.exists(), "No comment should be created for unauthenticated user.")

    def test_delete_comment_with_no_existing_comment(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
        data = {'content': 'This is a test comment'}
        
        # Realizar la solicitud
        response = self.client.delete(url, data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert 'error' in response.data
        
    def test_create_comment_with_no_existing_post(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-create-delete', kwargs={'post_id': 999})
        data = {'content': 'This is a test comment'}
        
        # Realizar la solicitud
        response = self.client.post(url, data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        assert 'error' in response.data
    
    def test_delete_comment_with_no_existing_post(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-create-delete', kwargs={'post_id': 999})
        data = {'content': 'This is a test comment'}
        
        # Realizar la solicitud
        response = self.client.delete(url, data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        assert 'error' in response.data

    def test_create_comment_with_no_content(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
        data = {'content': ''}
        
        # Realizar la solicitud
        response = self.client.post(url, data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        assert 'content' in response.data
        
    def test_delete_comment_as_authenticated_user_with_no_permissions(self):
        self.client = APIClient()
        force_authenticate(self.client,user=self.user)
        self.post.read_permission = 'team'
        self.post.edit_permission = 'team'
        self.post.author.team = 'Another team'
        self.post.author.save()
        self.post.save()
        url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
        data = {'content': 'This is a test comment'}
        
        # Realizar la solicitud
        response = self.client.delete(url, data)
        
        print(response.data)
        print(self.user.is_authenticated)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")
        self.assertFalse(Comment.objects.exists(), "No comment should be created for unauthenticated user.")
        
    def test_delete_comment_as_authenticated_user_with_read_permissions(self):
        self.client = APIClient()
        force_authenticate(self.client,user=self.user)
        self.post.read_permission = 'authenticated'
        self.post.edit_permission = 'authenticated'
        self.post.save()
        url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
        data = {'content': 'This is a test comment'}
        
        # Realizar la solicitud
        response = self.client.delete(url, data)
        
        print(self.user.is_authenticated)
        print(response.data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Comment.objects.exists(), "No comment should be created for unauthenticated user.")
        
            