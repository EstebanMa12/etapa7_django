
from comments.serializers import CommentSerializer
from .models import Comment
from rest_framework import generics, status
from rest_framework.permissions import IsAuthenticated
from avanzatech_blog.permissions import UserHasReadPermission
from django.shortcuts import get_object_or_404
from posts.models import Post
from rest_framework.response import Response
from django.db import IntegrityError
import django_filters
from django.db.models import Q, Subquery
from django.core.exceptions import ObjectDoesNotExist
from rest_framework.pagination import PageNumberPagination
from rest_framework.exceptions import PermissionDenied


# Create your views here.
class CommentCreateView(generics.GenericAPIView):
    """
    Vista para crear y eliminar comentarios
    """
    serializer_class = CommentSerializer
    permission_classes = [
        IsAuthenticated,
        UserHasReadPermission
    ]
    
    def get_object(self):
        """
        Obtiene el objeto Post correspondiente al post_id proporcionado en los parámetros de la URL.
        
        Returns:
            Post: El objeto Post correspondiente al post_id.
        """
        post_id = self.kwargs['post_id']
        return get_object_or_404(Post, id=post_id)
    
    def post(self, request, post_id):
        """
        Crea un comentario para un post.
        
        Args:
            request (HttpRequest): La solicitud HTTP recibida.
            post_id (int): El ID del post al que se desea agregar el comentario.
        
        Returns:
            Response: La respuesta HTTP con el resultado de la operación.
        """
        
        try:
            post = self.get_object()
            self.check_object_permissions(request, post) #Verificar permisos del objeto
        except PermissionDenied:
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        content = request.data.get('content')  # Obtener el contenido del comentario de la solicitud
        
        if not content:
            return Response({"error": "Content is required"}, status=status.HTTP_400_BAD_REQUEST)
        
        try:
            Comment.objects.create(user=request.user, post=post, content = content)
            return Response({"message": "Comment added successfully"}, status=status.HTTP_200_OK)  # return a 200 OK status
        except IntegrityError:
            return Response({"error": "Error creating comment"}, status=status.HTTP_400_BAD_REQUEST)
    
    def delete(self, request, post_id):
        """
        Elimina un comentario de un post.
        
        Args:
            request (HttpRequest): La solicitud HTTP recibida.
            post_id (int): El ID del post del que se desea eliminar el comentario.
        
        Returns:
            Response: La respuesta HTTP con el resultado de la operación.
        """
        try:
            post = self.get_object()
            self.check_object_permissions(request, post) #Verificar permisos del objeto
        except PermissionDenied:
            return Response({"error": "You do not have permission to perform this action."}, status=status.HTTP_403_FORBIDDEN)
        
        # Obtener el último comentario del post
        last_comment = Comment.objects.filter(post=post, user=request.user).order_by('-created_at').first()
        
        if last_comment:
            last_comment.delete()
            return Response({"message": "Comment deleted successfully"}, status=status.HTTP_200_OK)  # return a 200 OK status
        else:
            return Response({"error": "Comment does not exist"}, status=status.HTTP_400_BAD_REQUEST)


class CommentFilter(django_filters.FilterSet):
    """
        Filtro para los comentarios
    """
    post = django_filters.NumberFilter(field_name='post', lookup_expr='exact')
    user = django_filters.NumberFilter(field_name='user', lookup_expr='exact')
    
    class Meta:
        model = Comment
        fields = ['post', 'user']
        
class CommentListView(generics.ListAPIView):
    """
        Vista para listar los comentarios
    """
    serializer_class = CommentSerializer
    filterset_class = CommentFilter
    pagination_class = PageNumberPagination
    
    def get_queryset(self):
            """
            Obtiene el conjunto de consultas filtrado de comentarios según el usuario autenticado y los permisos de lectura.

            Returns:
                queryset (QuerySet): Conjunto de consultas filtrado de comentarios.
            """
            user = self.request.user
            try:
                if user.is_authenticated and user.is_admin:
                    queryset = CommentFilter(self.request.query_params, queryset=Comment.objects.all()).qs
                elif not user.is_authenticated:
                    allowed_posts = Post.objects.filter(read_permission='public')
                    queryset = CommentFilter(self.request.query_params, queryset=Comment.objects.filter(post_id__in=allowed_posts)).qs
                else:
                    allowed_posts = Post.objects.filter(
                        Q(read_permission='public') |
                        Q(read_permission='authenticated') |
                        Q(author=self.request.user) |
                        Q(author__team=self.request.user.team)
                    )
                    queryset = CommentFilter(self.request.query_params, queryset=Comment.objects.filter(post_id__in=allowed_posts)).qs
            except ObjectDoesNotExist:
                return Response({"detail": "No se encontraron posts permitidos"}, status=status.HTTP_404_NOT_FOUND)
            except Exception:
                # Handle any other exceptions
                return Response({"detail": "Ocurrió un error al procesar la solicitud"}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)

            return queryset
