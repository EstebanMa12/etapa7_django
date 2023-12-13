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

# a model for likes
class Like(DefaultModel, models.Model):
    # Like model
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)

    def __str__(self):
        return self.post.title + ' - ' + self.user.username
    
# a model for comments
class Comment(DefaultModel, models.Model):
    # Comment model
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.post.title + ' - ' + self.user.username + ' - ' + self.content[:20]