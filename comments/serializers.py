from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    """
    Serializer for the Comment model.
    """
    class Meta:
        model = Comment
        fields = ('post', 'user', 'content')
        
    def validate_content(self, value):
        """
        Validate the content of the comment.
        
        Args:
            value (str): The content of the comment.
        
        Returns:
            str: The validated content of the comment.
        
        Raises:
            serializers.ValidationError: If the content exceeds 1000 characters.
        """
        if len(value) > 1000:
            raise serializers.ValidationError('Content must be 1000 characters or less.')
        
        return value
    
    def create(self, validated_data):
        """
        Create a new comment instance.
        
        Args:
            validated_data (dict): The validated data for creating the comment.
        
        Returns:
            Comment: The newly created comment instance.
        """
        return Comment.objects.create(**validated_data)