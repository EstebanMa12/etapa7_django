import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from posts.models import Post
from tests.factories import LikesFactory, PostFactory, UserFactory
from likes.models import Like
pytestmark = pytest.mark.django_db


class TestPostCreateView(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        
    def test_create_post_as_admin(self):
        self.user.is_admin = True
        self.user.save()
        self.client.force_authenticate(self.user)
        
        self.assertTrue(self.user.is_authenticated)
        
        url = reverse('post-create')
        data = {'title': 'Test Post', 'content': 'This is a test post'}
        
        # Realizar la solicitud
        response = self.client.post(url, data)
        print(response.data)
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Post')
        self.assertEqual(response.data['content'], 'This is a test post')
        self.assertEqual(response.data['author'], self.user.id)
        
        
        self.assertEqual(Post.objects.count(), 1)   
        post = Post.objects.first()
        self.assertEqual(post.author, self.user)

    def test_create_post_as_authenticated_user(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('post-create')
        data = {'title': 'Test Post', 'content': 'This is a test post'}
        
        # Realizar la solicitud
        response = self.client.post(url, data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(response.data['title'], 'Test Post')
        self.assertEqual(response.data['content'], 'This is a test post')
        self.assertEqual(response.data['author'], self.user.id)
        
    def test_create_post_as_unauthenticated_user(self):
        url = reverse('post-create')
        data = {'title': 'Test Post', 'content': 'This is a test post'}
        
        # Realizar la solicitud
        response = self.client.post(url, data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")
        self.assertFalse(Post.objects.exists(), "No post should be created for unauthenticated user.")
        
    def test_create_post_with_invalid_data(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('post-create')
        data = {'title': '', 'content': 'This is a test post'}
        
        # Realizar la solicitud
        response = self.client.post(url, data)
        print(response.data['title'][0])
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['title'][0], "This field may not be blank.")
        self.assertFalse(Post.objects.exists(), "No post should be created with invalid data.")
    
    def test_edit_and_read_permissions_are_independent(self):
        self.post = PostFactory(read_permission='public', edit_permission='team')
        
        self.assertEqual(self.post.edit_permission, Post.TEAM)
        self.assertNotEqual(self.post.edit_permission,self.post.read_permission)
    
    def test_store_post_with_permissions_in_db(self):
        self.client.force_authenticate(user=self.user)
        url = reverse('post-create')
        data = {'title': 'Test Post', 'content': 'This is a test post'}
        
        response = self.client.post(url, data)
        
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        post = Post.objects.first()
        self.assertEqual(post.author, self.user)
        self.assertEqual(post.title, 'Test Post')
        self.assertEqual(post.content, 'This is a test post')
        self.assertEqual(post.read_permission, 'public')
        
#         Endpoint (`/blog/<post_id>`) for editing posts
        # Following fields can be changed
            # Permissions
            # Content
            # Title
        # Allow changes to content and visibility settings
        # Editing follows the permissions set on the post before the attempt to edit the post
        # Save changes in the database.
class TestPostEditView(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.post = PostFactory(author=self.user, read_permission="private")
        
    def test_update_post_as_authenticated_user_with_edit_permission(self):
            self.client.force_authenticate(user=self.user)
            url = reverse('post-edit', kwargs={'id': self.post.id})
            data = {'title': 'Updated Title', 'content': 'Updated Content'}
            
            # Realizar la solicitud
            response = self.client.put(url, data)
            
            # Verificar el comportamiento correcto
            self.assertEqual(response.status_code, status.HTTP_200_OK)
            self.post.refresh_from_db()
            self.assertEqual(self.post.title, 'Updated Title')
            self.assertEqual(self.post.content, 'Updated Content')

        def test_update_post_as_authenticated_user_without_edit_permission(self):
            user_without_permission = UserFactory()
            self.client.force_authenticate(user=user_without_permission)
            url = reverse('post-edit', kwargs={'id': self.post.id})
            data = {'title': 'Updated Title', 'content': 'Updated Content'}
            
            # Realizar la solicitud
            response = self.client.put(url, data)
            
            # Verificar el comportamiento correcto
            self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
            self.post.refresh_from_db()
            self.assertNotEqual(self.post.title, 'Updated Title')
            self.assertNotEqual(self.post.content, 'Updated Content')

        def test_update_post_with_invalid_data(self):
            self.client.force_authenticate(user=self.user)
            url = reverse('post-edit', kwargs={'id': self.post.id})
            data = {'title': '', 'content': 'Updated Content'}
            
            # Realizar la solicitud
            response = self.client.put(url, data)
            
            # Verificar el comportamiento correcto
            self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
            self.post.refresh_from_db()
            self.assertNotEqual(self.post.content, 'Updated Content')
        

        # Exists an endpoint (`/post` and `/post/<post_id>`) that allows users to view posts
        # The endpoint follows the permissions assigned to the user accessing the endpoint
        # The list endpoint will only include posts the user has access to in the list
            # Will return an empty list if there are no posts the user has access to
        # The details endpoint will return a 404 if the user does not have view access to the post
        # Pagination is implemented to limit the number of posts per page to 10. 
        # Pagination should include the following information: current page, total pages, total count, next page URL, previous page URL.

        # Possible to delete a blog post
        # Only a user with edit permission can delete a blog post
        # Upon deletion, the post is permanently removed from the database
        # All associated likes and comments are also deleted.




        
    # def test_list_posts_as_authenticated_user(self):
    #     self.client.force_authenticate(user=self.user)
    #     url = reverse('post-create')
        
    #     # Crear algunos posts
    #     PostFactory.create_batch(3)
        
    #     # Realizar la solicitud
    #     response = self.client.get(url)
    #     print(response.data)
    #     # Verificar el comportamiento correcto
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(response.data['count'], 3)
    #     self.assertEqual(response.data[0]['author'], self.user.id)
        
    # def test_list_posts_as_unauthenticated_user(self):
    #     url = reverse('post-create')
        
    #     # Crear algunos posts
    #     PostFactory.create_batch(3)
        
    #     # Realizar la solicitud
    #     response = self.client.get(url)
        
    #     # Verificar el comportamiento correcto
    #     self.assertEqual(response.status_code, status.HTTP_200_OK)
    #     self.assertEqual(len(response.data), 1)
    #     self.assertEqual(response.data[0]['read_permission'], 'public')