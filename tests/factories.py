import factory
from factory.django import DjangoModelFactory
from likes.models import Like
from user.models import CustomUser
from posts.models import Post
from comments.models import Comment

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
    
class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post
        
    title = factory.Faker('text', max_nb_chars=50)  # Update the max_nb_chars value to a shorter length
    content = factory.Faker('text', max_nb_chars=1000)  # Update the max_nb_chars value to a shorter length
    author = factory.SubFactory(UserFactory)
    read_permission = factory.Faker('random_element', elements=['public', 'authenticated', 'team', 'author'])
    edit_permission = factory.Faker('random_element', elements=['public', 'authenticated', 'team', 'author'])
    
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
