from rest_framework import serializers

from likes.models import Like

class LikeSerializer(serializers.ModelSerializer):
    class Meta:
        model = Like
        fields = ('post', 'user')
        
    def create(self, validated_data):
        return Like.objects.create(**validated_data)