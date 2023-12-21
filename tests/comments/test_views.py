import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from tests.factories import  CommentsFactory, PostFactory, UserFactory
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
        # print(response.data)
        
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
        self.client.force_authenticate(self.user)
        self.post.read_permission = 'team'
        self.post.edit_permission = 'team'
        self.post.author.team = 'Another team'
        self.post.author.save()
        self.post.save()
        url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
        data = {'content': 'This is a test comment'}
        
        # Realizar la solicitud
        response = self.client.post(url, data)

        
        # print(response.data)
        # print(self.user.is_authenticated)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], "You do not have permission to perform this action.")
        self.assertFalse(Comment.objects.exists(), "No comment should be created for unauthenticated user.")
        
    def test_create_comment_as_authenticated_user_with_read_permissions(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.post.read_permission = 'authenticated'
        self.post.edit_permission = 'authenticated'
        self.post.save()
        url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
        data = {'content': 'This is a test comment'}
        
        # Realizar la solicitud
        response = self.client.post(url, data)
        
        # print(self.user.is_authenticated)
        # print(response.data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertTrue(Comment.objects.exists(), "No comment should be created for unauthenticated user.")

    def test_delete_comment_as_authenticated_user(self):
        self.client.force_authenticate(self.user)
        url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
        data = {'content': 'This is a test comment'}
        
        # Crear un comentario
        self.client.post(url, data)
        
        # Realizar la solicitud
        response = self.client.delete(url, data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
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
        print(response.data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Comment does not exist")
        
    def test_create_comment_with_no_existing_post(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-create-delete', kwargs={'post_id': 999})
        data = {'content': 'This is a test comment'}
        
        # Realizar la solicitud
        response = self.client.post(url, data)
        print(response.data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
    
    def test_delete_comment_with_no_existing_post(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-create-delete', kwargs={'post_id': 999})
        data = {'content': 'This is a test comment'}
        
        # Realizar la solicitud
        response = self.client.delete(url, data)
        print(response.data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)

    def test_create_comment_with_no_content(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
        data = {'content': ''}
        
        # Realizar la solicitud
        response = self.client.post(url, data)
        print(response.data)
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Content is required")
        
    def test_delete_comment_as_authenticated_user_with_no_permissions(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.post.read_permission = 'team'
        self.post.edit_permission = 'team'
        self.post.author.team = 'Another team'
        self.post.author.save()
        self.post.save()
        url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
        data = {'content': 'This is a test comment'}
        
        # Realizar la solicitud
        response = self.client.delete(url, data)

        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], "You do not have permission to perform this action.")
        self.assertFalse(Comment.objects.exists(), "No comment should be created for unauthenticated user.")
        
    def test_delete_comment_as_authenticated_user_with_read_permissions(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.post.read_permission = 'authenticated'
        self.post.edit_permission = 'authenticated'
        self.post.save()
        url = reverse('comment-create-delete', kwargs={'post_id': self.post.id})
        data = {'content': 'This is a test comment'}
        
        # Crear un comentario
        self.client.post(url, data)
        
        # Realizar la solicitud
        response = self.client.delete(url, data)
        
        print(self.user.is_authenticated)
        print(response.data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Comment.objects.exists(), "No comment should be created for unauthenticated user.")
        
class TestCommentFilter(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.post = PostFactory(read_permission='public', edit_permission='public')

    def test_filter_comments_by_post(self):
        self.client.force_authenticate(self.user)
        url = reverse('comment-list')
        data = {'post': self.post.id}
        
        # Crear un comentario
        self.client.post(url, data)
        
        # Realizar la solicitud
        response = self.client.get(url, data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_filter_comments_by_user(self):
        self.client.force_authenticate(self.user)
        url = reverse('comment-list')
        data = {'user': self.user.id}
        
        # Crear un comentario
        self.client.post(url, data)
        
        # Realizar la solicitud
        response = self.client.get(url, data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_filter_comments_by_user_and_post(self):
        self.client.force_authenticate(self.user)
        url = reverse('comment-list')
        data = {'user': self.user.id, 'post': self.post.id}
        
        # Crear un comentario
        self.client.post(url, data)
        
        # Realizar la solicitud
        response = self.client.get(url, data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
        
class TestCommentListView(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.post = PostFactory(read_permission='public', edit_permission='public')

    def test_list_comments(self):
        self.client.force_authenticate(self.user)
        url = reverse('comment-list')
        
        # Crear un comentario
        self.client.post(url, {'content': 'This is a test comment', 'post': self.post.id})
        
        # Realizar la solicitud
        response = self.client.get(url)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        
    def test_list_comments_with_no_comments(self):
        self.client.force_authenticate(self.user)
        url = reverse('comment-list')
        
        # Realizar la solicitud
        response = self.client.get(url)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(len(response.data['results']), 0)
        
    def test_list_comments_with_no_authenticated_user(self):
        url = reverse('comment-list')

        # Crear un post con read_permission = 'public' y un comentario
        public_post = PostFactory(read_permission='public')
        CommentsFactory(user=self.user, post=public_post, content='This is a comment on a public post')

        # Crear un post con read_permission = 'authenticated' y un comentario
        private_post = PostFactory(read_permission='authenticated')
        CommentsFactory(user=self.user, post=private_post, content='This is a comment on a private post')

        # Realizar la solicitud
        response = self.client.get(url)
        print(response.data['results'][0]['content'])

        # Verificar que los comentarios del post público son visibles
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 1)
        self.assertEqual(response.data['results'][0]['content'], 'This is a comment on a public post')

        # Verificar que los comentarios del post privado no son visibles
        self.assertNotEqual(response.data['results'][0]['content'], 'This is a comment on a private post')
        
    def test_list_comments_as_authenticated_admin(self):
        self.user.is_admin = True
        self.user.save()
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-list')
        
        # Realizar la solicitud
        response = self.client.get(url)
        print(response.data['count'])
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Comment.objects.count())

    def test_list_comments_as_authenticated_user_with_permissions(self):
        self.client.force_authenticate(user=self.user)
        self.post.read_permission = 'authenticated'
        self.post.save()
        url = reverse('comment-list')
        
        # Realizar la solicitud
        response = self.client.get(url)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], Comment.objects.filter(post__read_permission__in=['public', 'authenticated']).count())

    def test_list_comments_as_authenticated_user_with_no_permissions(self):
        self.client.force_authenticate(user=self.user)
        self.post.read_permission = 'team'
        self.post.edit_permission = 'team'
        self.post.author.team = 'Another team'
        self.post.author.save()
        self.post.save()
        url = reverse('comment-list')
        
        # Realizar la solicitud
        response = self.client.get(url)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)

    def test_list_comments_with_invalid_query_params(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('comment-list')
        query_params = {'invalid_param': 'value'}
        
        # Realizar la solicitud
        response = self.client.get(url, query_params)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)