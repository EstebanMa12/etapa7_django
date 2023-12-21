import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient, APITestCase
from tests.factories import LikesFactory, PostFactory, UserFactory
from likes.models import Like
pytestmark = pytest.mark.django_db


class TestLikeCreateView(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.post = PostFactory(read_permission='public', edit_permission='public')

    def test_create_like_as_admin(self):
        admin_user = UserFactory(is_admin=True)
        self.client.force_authenticate(user=admin_user)

        url = reverse('like-create-delete', kwargs={'post_id': self.post.id})
        response = self.client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Like added successfully'

    def test_create_like_as_authenticated_user(self):
        self.client.force_authenticate(self.user)

        post = PostFactory(read_permission='public')

        url = reverse('like-create-delete', kwargs={'post_id': post.id})
        response = self.client.post(url)

        assert response.status_code == status.HTTP_200_OK
        assert response.data['message'] == 'Like added successfully'

    def test_create_like_as_unauthenticated_user(self):

        url = reverse('like-create-delete', kwargs={'post_id': self.post.id})
        response = self.client.post(url)
        
        print(response.data)

        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['detail'], "Authentication credentials were not provided.")
        self.assertFalse(Like.objects.exists(), "No comment should be created for unauthenticated user.")
    
    def test_create_like_as_authenticated_user_with_no_permissions(self):
        self.client = APIClient()
        self.client.force_authenticate(self.user)
        self.post.read_permission = 'team'
        self.post.edit_permission = 'team'
        self.post.author.team = 'Another team'
        self.post.author.save()
        self.post.save()
        
        url = reverse('like-create-delete', kwargs={'post_id': self.post.id})
        
        response = self.client.post(url)
        
        print(response.data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], "You do not have permission to perform this action.")
        self.assertFalse(Like.objects.exists(), "No comment should be created for unauthenticated user.")
        
    def test_create_like_as_authenticated_user_with_read_permissions(self):
        self.client.force_authenticate(self.user)
        self.post.read_permission = 'team'
        self.post.edit_permission = 'team'
        self.post.author.team = self.user.team
        self.post.author.save()
        self.post.save()
        
        url = reverse('like-create-delete', kwargs={'post_id': self.post.id})
        
        response = self.client.post(url)
        
        print(response.data)
        
        # Verificar el comportamiento correcto
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Like added successfully")
        self.assertTrue(Like.objects.exists(), "No comment should be created for unauthenticated user.")
    
    def test_delete_like_as_authenticated_user(self):
        self.client.force_authenticate(self.user)
        url = reverse('like-create-delete', kwargs={'post_id': self.post.id})
        
        #Crear el like
        self.client.post(url)
        
        #Eliminar el like
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Like deleted successfully")
        
        #Verificar que el like se eliminó
        self.assertFalse(Like.objects.exists(), "No like should be created for unauthenticated user.")
        
    def test_delete_like_as_authenticated_user_with_no_permissions(self):
        self.client.force_authenticate(self.user)
        self.post.read_permission = 'team'
        self.post.edit_permission = 'team'
        self.post.author.team = 'Another team'
        self.post.author.save()
        self.post.save()
        
        url = reverse('like-create-delete', kwargs={'post_id': self.post.id})
        
        #Crear el like
        self.client.post(url)
        
        #Eliminar el like
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_403_FORBIDDEN)
        self.assertEqual(response.data['error'], "You do not have permission to perform this action.")
        
        #Verificar que el like no se eliminó
        self.assertFalse(Like.objects.exists(), "No like should be created for unauthenticated user.")
        
    def test_delete_like_with_no_existing_like(self):
        self.client.force_authenticate(self.user)
        url = reverse('like-create-delete', kwargs={'post_id': self.post.id})
        
        #Eliminar el like
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_400_BAD_REQUEST)
        self.assertEqual(response.data['error'], "Like does not exist")
        
        #Verificar que el like se eliminó
        self.assertFalse(Like.objects.exists(), "The like should not be deleted as it does not exist.")
        
    def test_create_like_with_no_existing_post(self):
        self.client.force_authenticate(self.user)
        url = reverse('like-create-delete', kwargs={'post_id': 999})
        
        #Eliminar el like
        response = self.client.post(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Not found.")
        
        #Verificar que el like se eliminó
        self.assertFalse(Like.objects.exists(), "The like should not be created as the post does not exist.")
        
    def test_delete_like_with_no_existing_post(self):
        self.client.force_authenticate(self.user)
        url = reverse('like-create-delete', kwargs={'post_id': 999})
        
        #Eliminar el like
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_404_NOT_FOUND)
        self.assertEqual(response.data['detail'], "Not found.")
        
        #Verificar que el like se eliminó
        self.assertFalse(Like.objects.exists(), "The like should not be deleted as the post does not exist.")
    
    def test_delete_comment_as_authenticated_user_with_read_permissions(self):
        self.client.force_authenticate(self.user)
        self.post.read_permission = 'team'
        self.post.edit_permission = 'team'
        self.post.author.team = self.user.team
        self.post.author.save()
        self.post.save()
        
        url = reverse('like-create-delete', kwargs={'post_id': self.post.id})
        
        #Crear el like
        self.client.post(url)
        
        #Eliminar el like
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['message'], "Like deleted successfully")
        
        #Verificar que el like se eliminó
        self.assertFalse(Like.objects.exists(), "The like should be deleted as the user have read permissions")
        
        


class TestLikeListView(APITestCase):
    def setUp(self):
        self.user = UserFactory()
        self.client = APIClient()
        self.post = PostFactory(read_permission='public', edit_permission='public')

    def test_get_likes_as_admin(self):
        admin_user = UserFactory(is_admin=True)
        self.client.force_authenticate(user=admin_user)

        # Crear algunos likes para probar
        LikesFactory.create_batch(3)

        url = reverse('like-list')
        response = self.client.get(url)
        
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['count'],3)

    def test_get_likes_as_authenticated_user(self):
        self.client.force_authenticate(self.user)

        # Crear algunos likes para probar
        allowed_posts = PostFactory.create_batch(2, read_permission='public')
        LikesFactory.create_batch(3, post=allowed_posts[0])
        LikesFactory.create_batch(2, post=allowed_posts[1])

        url = reverse('like-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)

    def test_get_likes_as_unauthenticated_user(self):

        # Crear algunos likes para probar
        allowed_posts = PostFactory.create_batch(2, read_permission='public')
        LikesFactory.create_batch(3, post=allowed_posts[0])
        LikesFactory.create_batch(2, post=allowed_posts[1])

        url = reverse('like-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)
    
    def test_get_likes_as_authenticated_user_with_no_permissions(self):
        self.client.force_authenticate(self.user)
        self.post.read_permission = 'team'
        self.post.edit_permission = 'team'
        self.post.author.team = 'Another team'
        self.post.author.save()
        self.post.save()
        
        # Crear algunos likes para probar
        allowed_posts = PostFactory.create_batch(2, read_permission='team')
        LikesFactory.create_batch(3, post=allowed_posts[0])
        LikesFactory.create_batch(2, post=allowed_posts[1])

        url = reverse('like-list')
        response = self.client.get(url)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 0)
    
    def test_get_likes_as_authenticated_user_with_read_permissions(self):
        self.client.force_authenticate(self.user)
        self.post.read_permission = 'team'
        self.post.edit_permission = 'team'
        self.post.author.team = self.user.team
        self.post.author.save()
        self.post.save()

        # Verificar que los permisos se guardaron correctamente
        self.assertEqual(self.post.read_permission, 'team')
        self.assertEqual(self.post.edit_permission, 'team')
        self.assertEqual(self.post.author.team, self.user.team)

        # Crear algunos likes para probar
        allowed_posts = PostFactory.create_batch(2, read_permission='team', author__team=self.user.team)
        LikesFactory.create_batch(3, post=allowed_posts[0])
        LikesFactory.create_batch(2, post=allowed_posts[1])

        # Verificar que los likes se crearon correctamente
        self.assertEqual(Like.objects.count(), 5)

        url = reverse('like-list')
        response = self.client.get(url)
        print(response.data)

        self.assertEqual(response.status_code,status.HTTP_200_OK)
        self.assertEqual(response.data['count'], 5)