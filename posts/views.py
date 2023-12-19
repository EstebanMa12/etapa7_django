
# POSTS
from django.http import Http404
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from posts.models import Post
from posts.serializers import PostSerializer
from django.core.exceptions import ValidationError
from avanzatech_blog.permissions import UserHasEditPermission, UserHasReadPermission, IsCustomAdminUser
from rest_framework.pagination import PageNumberPagination
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import PermissionDenied
from django.db.models import Q, Subquery

# View for create POST and List

class PostCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    
    def get_permissions(self):
        if self.request.method == 'POST':
            return [IsAuthenticated()]
        return super().get_permissions()
    
    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        user = self.request.user

        if user.is_authenticated and user.is_admin:
            # Admin has all permissions, return all posts
            return Post.objects.all()
        
        try:
            allowed_posts = Post.objects.filter(
                Q(read_permission=Post.PUBLIC) |
                Q(read_permission=Post.AUTHENTICATED) |
                Q(author=user) |
                Q(author__team=user.team)
            )

            queryset = super().get_queryset().filter(id__in=Subquery(allowed_posts.values('id')))
            
            return queryset
        
        except ObjectDoesNotExist as e:
            # Manejo de la excepción cuando no se encuentran posts permitidos
            return Response({"detail": "No se encontraron posts permitidos"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            # Manejo de otras excepciones
            return Response({"detail": "Ocurrió un error al procesar la solicitud"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
            
        

# View for edit POST
class PostEditView(generics.UpdateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [IsAuthenticated,UserHasEditPermission]
    lookup_field = 'id'
    
    def perform_update(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
        
class PostDetailView(generics.RetrieveAPIView):
    """
        Vista para ver un post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    permission_classes = [IsAuthenticated]
    
    def get_object(self):
        obj = super().get_object()
        permissions  = UserHasReadPermission()
        if not permissions.has_object_permission(self.request,self, obj):
            raise PermissionDenied("No tienes permiso para ver este post")
        return obj

# DELETE POST
class PostDeleteView(generics.DestroyAPIView):
    """
        Vista para eliminar un post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    permission_classes = [
        IsAuthenticated,
        UserHasEditPermission
        ]
    
    def destroy(self, request, *args, **kwargs):
        try:
            post = self.get_object()
            self.check_object_permissions(request, post)
            post.delete()
            return Response({"message": "Post deleted successfully"}, status=status.HTTP_200_OK)
        except Http404:
            return Response({"error": "Post doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)


