import factory
from factory.django import DjangoModelFactory
from likes.models import Like
from user.models import CustomUser
from posts.models import Post
from comments.models import Comment
from django.core.exceptions import ValidationError

class UserFactory(DjangoModelFactory):
    class Meta:
        model = CustomUser

    username = factory.Sequence(lambda n: 'user{}'.format(n))
    password = factory.PostGenerationMethodCall('set_password', 'password')
    team = factory.Sequence(lambda n: 'team{}'.format(n))
    is_admin = False
    is_superuser = False
    
    @classmethod
    def create_superuser(cls, **kwargs):
        return cls.create(is_admin=True, is_superuser=True, team="SuperUser", **kwargs)

# This is for test the serializers and models
class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post
        
    title = factory.Faker('text', max_nb_chars=50)  # Update the max_nb_chars value to a shorter length
    content = factory.Faker('text', max_nb_chars=1000)  # Update the max_nb_chars value to a shorter length
    author = factory.SubFactory(UserFactory)
    read_permission = factory.Faker('random_element', elements=['public', 'authenticated', 'team', 'author'])
    edit_permission = factory.Faker('random_element', elements=['public', 'authenticated', 'team', 'author'])
    
    @factory.post_generation
    def check_permissions(obj, create, extracted, **kwargs):
        if obj.read_permission not in dict(Post.PERMISSIONS).keys() or obj.edit_permission not in dict(Post.PERMISSIONS).keys():
            raise ValidationError('Invalid permission specified.')
    
class LikesFactory(DjangoModelFactory):
    class Meta:
        model = Like
        
    post = factory.SubFactory(PostFactory)
    user = factory.SubFactory(UserFactory)
    
class CommentsFactory(DjangoModelFactory):
    class Meta:
        model = Comment
        
    post = factory.SubFactory(PostFactory)
    user = factory.SubFactory(UserFactory)
    content = factory.Sequence(lambda n: 'content{}'.format(n))