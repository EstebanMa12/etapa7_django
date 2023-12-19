from rest_framework import serializers
from .models import Comment

class CommentSerializer(serializers.ModelSerializer):
    class Meta:
        model = Comment
        fields = ('post', 'user', 'content')
        
    def validate_content(self, value):
        # Validación para longitud del contenido
        if len(value) > 1000:
            raise serializers.ValidationError('Content must be 1000 characters or less.')
        
        return value
    
    def create(self, validated_data):
        return Comment.objects.create(**validated_data)