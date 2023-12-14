from django.db import models

from user.models import CustomUser, DefaultModel

# Create your models here.
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
    read_permission = models.CharField(max_length=20, choices=PERMISSIONS, default=PUBLIC)
    edit_permission = models.CharField(max_length=20, choices=PERMISSIONS, default=PUBLIC)
    
    def __str__(self):
        return self.title
    class Meta:
        ordering = ['-created_at']