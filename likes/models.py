from django.db import models

from posts.models import Post
from user.models import CustomUser, DefaultModel

# Create your models here.
# a model for likes
class Like(DefaultModel, models.Model):
    # Like model
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    
    class Meta:
        unique_together = ('post', 'user')

    def __str__(self):
        return self.post.title + ' - ' + self.user.username