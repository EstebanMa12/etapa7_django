

# Create your views here.
# POSTS
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated, BasePermission
from posts.models import Post
from posts.serializers import PostSerializer
from django.core.exceptions import ValidationError

class AdminHasEditPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Comprueba cuales son los permisos de edicion del post
        if obj.edit_permission == Post.PUBLIC:
            return True
        elif obj.edit_permission == Post.AUTHENTICATED:
            return request.user.is_authenticated
        elif obj.edit_permission == Post.TEAM:
            return request.user.team == obj.author.team
        elif obj.edit_permission == Post.AUTHOR:
            return request.user == obj.author
        else:
            return False
        
class AdminHasReadPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Comprueba cuales son los permisos de lectura del post
        if obj.read_permission == Post.PUBLIC:
            return True
        elif obj.read_permission == Post.AUTHENTICATED:
            return request.user.is_authenticated
        elif obj.read_permission == Post.TEAM:
            return request.user.team == obj.author.team
        elif obj.read_permission == Post.AUTHOR:
            return request.user == obj.author
        else:
            return False


# View for create POST
class PostCreateView(generics.CreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated]
    
    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)

# View for edit POST
class PostEditView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [AdminHasEditPermission]
    lookup_field = 'id'
    
    def perform_update(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
