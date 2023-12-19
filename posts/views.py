
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
from rest_framework import serializers

# View for create POST and List

class PostCreateView(generics.ListCreateAPIView):
    """
        Vista para la creación y listado de post a los que tengo permiso
    """
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    
    def get_permissions(self):
        return [IsAuthenticated()]
    
    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        user = self.request.user
        try:
            if user.is_authenticated and user.is_admin:
                # Admin has all permissions, return all posts
                queryset= Post.objects.all()
            # If not authenticated only view the post with read_permissions=='public'
            elif not user.is_authenticated:
                queryset= Post.objects.filter(read_permission=Post.PUBLIC)
        
            else:
                allowed_posts = Post.objects.filter(
                Q(read_permission=Post.PUBLIC) |
                Q(read_permission=Post.AUTHENTICATED) |
                Q(author=user) |
                Q(author__team=user.team)
            )

                queryset = Post.objects.filter(id__in=Subquery(allowed_posts.values('id')))
            
        except ObjectDoesNotExist:
            # Manejo de la excepción cuando no se encuentran posts permitidos
            return Response({"detail": "No se encontraron posts permitidos"}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            print(f"Excepcion {str(e)}")
            # Manejo de otras excepciones
            return Response({"detail": "Ocurrió un error al procesar la solicitud"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        
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
    """
        Vista para ver un solo post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'id'
    permission_classes = [UserHasReadPermission]
    
    def get_object(self):
        # post_id = self.kwargs['id']
        # return get_object_or_404(Post, id=post_id)
        
        obj = super().get_object()

        # Verificar los permisos personalizados
        permissions = UserHasReadPermission()

        if not permissions.has_object_permission(self.request, self, obj):
            raise PermissionDenied("No tienes permiso para ver este post")

        return obj

# DELETE POST
class PostDeleteView(generics.DestroyAPIView):
    """
        Vista para eliminar un post
    """
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    lookup_field = 'pk'
    permission_classes = [
        UserHasEditPermission
        ]
    
    def destroy(self, request, *args, **kwargs):
        try:
            post = self.get_object()
            permissions = UserHasEditPermission()
            
            if not permissions.has_object_permission(request, self, post):
                raise PermissionDenied("No tienes permiso para eliminar este post")
            
            self.perform_destroy(post)
            return self.get_response()
        except Http404:
            return Response({"error": "Post doesn't exist"}, status=status.HTTP_400_BAD_REQUEST)
        
    def get_response(self):
                return Response({"message": "Post deleted successfully"}, status=status.HTTP_200_OK)


