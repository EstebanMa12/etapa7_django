from django.db import models

from posts.models import Post
from user.models import CustomUser, DefaultModel

# Create your models here.
# a model for likes
class Like(DefaultModel, models.Model):
    """
    Represents a like on a post by a user.
    """

    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return self.post.title + ' - ' + self.user.username
    
    def clean(self):
        if self.post is None:
            raise ValueError('Likes must have a post')
        if self.user is None:
            raise ValueError('Likes must have a user')
    