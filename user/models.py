from django.contrib.auth.models import AbstractUser
from django.db import models

# A default model with the created_at, modified_at, is_deleted field
class DefaultModel(models.Model):
    created_at = models.DateTimeField(auto_now_add=True)
    modified_at = models.DateTimeField(auto_now=True)
    is_deleted = models.BooleanField(default=False)

    class Meta:
        abstract = True
        
class Team(DefaultModel, models.Model):
    # Teams model
    team_name = models.CharField(max_length=100)

    def __str__(self):
        return self.team_name

class CustomUser(AbstractUser):
    # Use email as the username field
    username = models.EmailField(unique=True)
    team = models.ForeignKey(Team, on_delete=models.CASCADE, blank=True, default=None, null=True)

    USERNAME_FIELD = 'username'
    REQUIRED_FIELDS = ['password']

    def __str__(self):
        return self.email
    

# a model for Posts
class Post(DefaultModel, models.Model):
    # Post model
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
    content = models.TextField()
    author = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    permission = models.CharField(max_length=20, choices=PERMISSIONS, default=PUBLIC)
    def __str__(self):
        return self.title

