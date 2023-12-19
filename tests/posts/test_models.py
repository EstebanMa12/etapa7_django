from django.test import TestCase
from ...posts.models import Post

class PostModelTest(TestCase):
    @classmethod
    def setUpTestData(cls):
        # Crear un objeto Post para usarlo en las pruebas
        Post.objects.create(
            title='Título de prueba',
            content='Contenido de prueba',
            author_id=1,
            read_permission=Post.PUBLIC,
            edit_permission=Post.PUBLIC
        )

    def test_str_representation(self):
        post = Post.objects.get(id=1)
        self.assertEqual(str(post), 'Título de prueba')

    def test_ordering(self):
        # Crear más objetos Post para probar el ordenamiento
        Post.objects.create(
            title='Título 1',
            content='Contenido 1',
            author_id=1,
            read_permission=Post.PUBLIC,
            edit_permission=Post.PUBLIC
        )
        Post.objects.create(
            title='Título 2',
            content='Contenido 2',
            author_id=1,
            read_permission=Post.PUBLIC,
            edit_permission=Post.PUBLIC
        )

        posts = Post.objects.all()
        self.assertEqual(posts[0].title, 'Título de prueba')
        self.assertEqual(posts[1].title, 'Título 2')
        self.assertEqual(posts[2].title, 'Título 1')