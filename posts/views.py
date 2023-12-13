
# POSTS
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from posts.models import Post
from posts.serializers import PostSerializer
from django.core.exceptions import ValidationError
from .permissions import UserHasEditPermission, UserHasReadPermission


# View for create POST and List
class PostCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    
    def get_permissions(self):
        permissions = []
        if self.request.method == 'POST':
            permissions.append(IsAuthenticated)
            # self.permission_classes = [IsAuthenticated,]
        else:
            permissions.append(UserHasReadPermission)
            # self.permission_classes = [UserHasReadPermission,]
        return [p() for p in permissions]      
    
    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
    def get(self, request, *args, **kwargs):        
        posts = self.queryset.all()
        serializer = PostSerializer(posts, many=True)
        return Response(serializer.data)

# View for edit POST
class PostEditView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [UserHasEditPermission]
    lookup_field = 'id'
    
    def perform_update(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

