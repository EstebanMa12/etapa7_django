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
    team = factory.Sequence(lambda n: 'team{}'.format(n))
    is_superuser = False
    is_admin = False
    password = factory.PostGenerationMethodCall('set_password', 'password')
    
class PostFactory(DjangoModelFactory):
    class Meta:
        model = Post
        
    title = factory.Sequence(lambda n: 'title{}'.format(n))
    content = factory.Sequence(lambda n: 'content{}'.format(n))
    author = factory.SubFactory(UserFactory)
    read_permission = 'public'
    edit_permission = 'public'
    
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
