from rest_framework import serializers

from likes.models import Like

class LikeSerializer(serializers.ModelSerializer):
    """
    Serializer for the Like model.
    """
    class Meta:
        model = Like
        fields = ('post', 'user')
        
    def create(self, validated_data):
        """
        Create and return a new Like instance.
        
        Args:
            validated_data (dict): Validated data for creating a Like instance.
            
        Returns:
            Like: The newly created Like instance.
        """
        return Like.objects.create(**validated_data)