from django.db import models

from user.models import CustomUser, DefaultModel

# Create your models here.
# a model for Posts
class Post(DefaultModel, models.Model):
    """
    Represents a post in the application.

    Attributes:
        PUBLIC (str): Constant representing public permission.
        AUTHENTICATED (str): Constant representing authenticated permission.
        TEAM (str): Constant representing team permission.
        AUTHOR (str): Constant representing author permission.
        PERMISSIONS (tuple): Tuple of permission choices.
        title (str): The title of the post.
        content (str): The content of the post.
        author (CustomUser): The author of the post.
        read_permission (str): The read permission for the post.
        edit_permission (str): The edit permission for the post.
    """

    PUBLIC = 'public'
    AUTHENTICATED = 'authenticated'
    TEAM = 'team'
    AUTHOR = 'author'
    
    PERMISSIONS = (
        (PUBLIC, 'Public'),
        (AUTHENTICATED, 'Authenticated'),
        (TEAM, 'Team'),
        (AUTHOR, 'Author'),
    )
    
    title = models.CharField(max_length=100)
    content = models.TextField(max_length=1000)
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    read_permission = models.CharField(max_length=20, choices=PERMISSIONS, default=PUBLIC)
    edit_permission = models.CharField(max_length=20, choices=PERMISSIONS, default=PUBLIC)
    
    def __str__(self):
        return self.title
    
    class Meta:
        ordering = ['-created_at']