import pytest
from django.urls import reverse
from rest_framework import status
from rest_framework.test import APIClient
from tests.factories import LikesFactory, PostFactory, UserFactory

pytestmark = pytest.mark.django_db

class TestLikeListView:

    def test_get_likes_as_admin(self):
        admin_user = UserFactory(is_admin=True)
        client = APIClient()
        client.force_authenticate(user=admin_user)

        # Crear algunos likes para probar
        LikesFactory.create_batch(3)

        url = reverse('like-list')
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 3

    def test_get_likes_as_authenticated_user(self):
        user = UserFactory()
        client = APIClient()
        client.force_authenticate(user=user)

        # Crear algunos likes para probar
        allowed_posts = PostFactory.create_batch(2, read_permission='public')
        LikesFactory.create_batch(3, post=allowed_posts[0])
        LikesFactory.create_batch(2, post=allowed_posts[1])

        url = reverse('like-list')
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5

    def test_get_likes_as_unauthenticated_user(self):
        client = APIClient()

        # Crear algunos likes para probar
        allowed_posts = PostFactory.create_batch(2, read_permission='public')
        LikesFactory.create_batch(3, post=allowed_posts[0])
        LikesFactory.create_batch(2, post=allowed_posts[1])

        url = reverse('like-list')
        response = client.get(url)

        assert response.status_code == status.HTTP_200_OK
        assert len(response.data) == 5

    def test_get_likes_with_error(self):
        client = APIClient()

        # Simular un error al procesar la solicitud
        url = reverse('like-list')
        response = client.get(url)

        assert response.status_code == status.HTTP_500_INTERNAL_SERVER_ERROR
        assert 'detail' in response.data