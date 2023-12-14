
from sqlite3 import IntegrityError
from django.shortcuts import get_object_or_404
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from likes.models import Like
from posts.models import Post
from likes.serializers import LikeSerializer
from posts.permissions import UserHasReadPermission
from django.db import IntegrityError
from rest_framework.pagination import PageNumberPagination


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
        post_id = self.kwargs['post_id']
        return get_object_or_404(Post, id=post_id)
    
    def post(self, request, post_id):
        """
        Crea un like para un post.
        """
        post = self.get_object()
        self.check_object_permissions(request, post) #Verificar permisos del objeto
        
        try:
            Like.objects.create(user=request.user, post=post)
            return Response({"message": "Like added successfully"}, status=status.HTTP_200_OK)  # return a 200 OK status
        except IntegrityError:
            return Response({"error": "Like already exists"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id):
        """
        Elimina un like de un post.
        """
        post = self.get_object()
        self.check_object_permissions(request, post) #Verificar permisos del objeto
        
        try:
            Like.objects.filter(user=request.user, post=post).delete()
            return Response({"message": "Like deleted successfully"}, status=status.HTTP_200_OK)  # return a 200 OK status
        except IntegrityError:
            return Response({"error": "Like does not exist"}, status=status.HTTP_400_BAD_REQUEST)




# FILTERS OF LIKES 

import django_filters
class LikeFilter(django_filters.FilterSet):
    """
        Filtro para los likes
    """
    user_id = django_filters.NumberFilter(field_name='id', lookup_expr='exact')
    post_id = django_filters.NumberFilter(field_name='id', lookup_expr='exact')
    class Meta:
        model = Like
        fields = ['user_id', 'post_id']

        
# LIST OF LIKES
class LikeListView(generics.ListAPIView):
    """
        Vista para ver los likes a los cuales tengo permiso
    """
    serializer_class = LikeSerializer
    permission_classes = [
        IsAuthenticated,
        UserHasReadPermission
    ]    
    pagination_class = PageNumberPagination
    filter_class = LikeFilter 
    
    def get_queryset(self):
        queryset = Like.objects.filter(post__user=self.request.user)  # Solo los likes de los posts del usuario autenticado
        user_id = self.request.query_params.get('user_id')
        print(user_id)
        post_id = self.request.query_params.get('post_id')
        if user_id is not None:
            try:
                user_id = int(user_id)
                queryset = queryset.filter(user__id=user_id)
            except (ValueError, TypeError):
                return Like.objects.none()
            
        if post_id is not None:
            try:
                post_id = int(post_id)
                queryset = queryset.filter(post__id=post_id)
            except (ValueError, TypeError):
                return Like.objects.none()
        return queryset