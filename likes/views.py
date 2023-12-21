
from django.shortcuts import get_object_or_404
from rest_framework import status, generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from likes.models import Like
from posts.models import Post
from likes.serializers import LikeSerializer
from avanzatech_blog.permissions import UserHasReadPermission, IsCustomAdminUser
from django.db import IntegrityError
from rest_framework.pagination import PageNumberPagination
from django.db.models import Q, Subquery
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.exceptions import PermissionDenied


# Create your views here.
class LikeCreateView(generics.GenericAPIView):
    """
    Vista para crear y eliminar likes
    """

    serializer_class = LikeSerializer
    permission_classes = [
        IsAuthenticated,
        UserHasReadPermission
    ]
    
    def get_object(self):
        """
        Obtiene el objeto Post correspondiente al post_id proporcionado en los parámetros de la URL.
        """
        post_id = self.kwargs['post_id']
        return get_object_or_404(Post, id=post_id)
    
    def post(self, request, post_id):
        """
        Crea un like para un post.
        """
        try:
            post = self.get_object()
            self.check_object_permissions(request, post) #Verificar permisos del objeto
        except PermissionDenied:
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        try:
            Like.objects.create(user=request.user, post=post)
            return Response({"message": "Like added successfully"}, status=status.HTTP_200_OK)  # return a 200 OK status
        except IntegrityError:
            return Response({"error": "Like already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id):
        """
        Elimina un like de un post.
        """
        try:
            post = self.get_object()
            self.check_object_permissions(request, post) #Verificar permisos del objeto
        except PermissionDenied:
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        like = Like.objects.filter(user=request.user, post=post)
        if not like.exists():
            return Response({"error": "Like does not exist"}, status=status.HTTP_400_BAD_REQUEST)

        like.delete()
        return Response({"message": "Like deleted successfully"}, status=status.HTTP_200_OK)  # return a 200 OK status


# FILTERS OF LIKES 

import django_filters
class LikeFilter(django_filters.FilterSet):
    """
        Filtro para los likes
    """
    user_id = django_filters.NumberFilter(field_name='user__id', lookup_expr='exact')
    post_id = django_filters.NumberFilter(field_name='post__id', lookup_expr='exact')
    class Meta:
        model = Like
        fields = ['user_id', 'post_id']

class CustomPagination(PageNumberPagination):
    """
        Paginación personalizada
    """
    page_size = 20
    page_size_query_param = 'page_size'
    max_page_size = 100
# LIST OF LIKES
class LikeListView(generics.ListAPIView):
    """
        Vista para ver los likes de los post a los cuales tengo permiso
    """
    serializer_class = LikeSerializer
    pagination_class = CustomPagination
    filter_class = LikeFilter 
    
    def get_queryset(self):
        user = self.request.user

        try:
            if user.is_authenticated and user.is_admin:
                queryset = LikeFilter(self.request.query_params, queryset=Like.objects.all()).qs
            elif not user.is_authenticated:
                allowed_posts = Post.objects.filter(read_permission='public')
                queryset = LikeFilter(self.request.query_params, queryset=Like.objects.filter(post_id__in=allowed_posts)).qs
            else:
                allowed_posts = Post.objects.filter(
                    Q(read_permission='public') |
                    Q(read_permission='authenticated') |
                    Q(author=self.request.user) |
                    Q(author__team=self.request.user.team)
                )
                queryset = LikeFilter(self.request.query_params, queryset=Like.objects.filter(post_id__in=allowed_posts)).qs
        except ObjectDoesNotExist:
            return Response({"detail": "No se encontraron posts permitidos"}, status=status.HTTP_404_NOT_FOUND)
        except Exception:
            # Handle any other exceptions
            return Response({"detail": "Ocurrió un error al procesar la solicitud"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

        return queryset
    
