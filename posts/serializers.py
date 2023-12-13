
from posts.models import Post
from rest_framework import serializers



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title',
                'content',
                'author',
                'read_permission', 
                'edit_permission')