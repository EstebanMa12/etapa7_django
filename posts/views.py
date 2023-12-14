
# POSTS
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from posts.models import Post
from posts.serializers import PostSerializer
from django.core.exceptions import ValidationError
from .permissions import UserHasEditPermission, UserHasReadPermission
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import PermissionDenied


# View for create POST and List
class PostCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    
    def get_permissions(self):
        permissions = []
        if self.request.method == 'POST':
            permissions.append(IsAuthenticated)
        else:
            permissions.append(UserHasReadPermission)
        return [p() for p in permissions]      
    
    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        try:    
            queryset = Post.objects.all()
            # Filtrado
            for post in list(queryset):
                object_permissions  = UserHasReadPermission()
                if not object_permissions.has_object_permission(self.request, self, post):
                    queryset = queryset.exclude(id=post.id)
        except ObjectDoesNotExist:
            queryset = Post.objects.none()
        except Exception as e:
            print(f"Error al obtener los posts: {e}")
            queryset = Post.objects.none()
            
        return queryset

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
        
class PostDetailView(generics.RetrieveAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    
    def get_object(self):
        obj = super().get_object()
        permissions  = UserHasReadPermission()
        if not permissions.has_object_permission(self.request,self, obj):
            raise PermissionDenied("No tienes permiso para ver este post")
        return obj
        
#LIKES

from posts.models import Like
from user.models import CustomUser

def add_like(request, post_id):
    user = CustomUser.objects.get(id=request.user.id)
    post = Post.objects.get(post_id)
    like = Like(user=user, post=post)
    like.save()

def remove_like(request, post_id):
    user = CustomUser.objects.get(id=request.user.id)
    post = Post.objects.get(post_id)
    like = Like.objects.get(user=user, post=post)
    like.delete()

