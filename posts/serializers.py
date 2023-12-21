
from posts.models import Post
from rest_framework import serializers



class PostSerializer(serializers.ModelSerializer):
    """
    Serializer for the Post model.

    This serializer is used to convert Post instances into JSON
    representation and vice versa. It defines the fields that should
    be included in the serialized output and provides methods for
    updating existing Post instances.

    Attributes:
        model (Post): The Post model class.
        fields (tuple): The fields to include in the serialized output.
        read_only_fields (tuple): The fields that should be read-only.

    Methods:
        update(instance, validated_data): Updates an existing Post instance.

    """
    class Meta:
        model = Post
        fields = ('title',
                  'content',
                  'read_permission',
                  'edit_permission',
                  'author',)
        read_only_fields = (
            'author',
        )
    
    def update(self, instance, validated_data):
        instance.title = validated_data.get('title', instance.title)
        instance.content = validated_data.get('content', instance.content)
        instance.read_permission = validated_data.get('read_permission', instance.read_permission)
        instance.edit_permission = validated_data.get('edit_permission', instance.edit_permission)
        instance.save()
        return instance