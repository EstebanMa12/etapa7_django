
from posts.forms import PostForm
from posts.models import Post
from rest_framework import serializers



class PostSerializer(serializers.ModelSerializer):
    class Meta:
        model = Post
        fields = ('title',
                'content',
                'read_permission', 
                'edit_permission')
        
    def create(self, validated_data):
        return Post.objects.create(**validated_data)
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.read_permission = validated_data.get('read_permission', instance.read_permission)
        instance.edit_permission = validated_data.get('edit_permission', instance.edit_permission)
        instance.save()
        return instance