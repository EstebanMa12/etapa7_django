from django.db import models
from django.core.exceptions import ValidationError
from posts.models import Post
from user.models import CustomUser, DefaultModel

# Create your models here.
# a model for comments
class Comment(DefaultModel, models.Model):
    # Comment model
    post = models.ForeignKey(Post, on_delete=models.CASCADE)
    user = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    content = models.TextField()

    def __str__(self):
        return self.post.title + ' - ' + self.user.username + ' - ' + self.content[:20]

    def clean(self):
        if not self.post:
            raise ValidationError("Post does not exist.")
        if not self.user:
            raise ValidationError("User does not exist.")
        if not self.content:
            raise ValidationError("Content cannot be empty.")
