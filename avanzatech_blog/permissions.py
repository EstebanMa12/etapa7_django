from rest_framework.permissions import BasePermission, DjangoObjectPermissions
from posts.models import Post
class UserHasEditPermission(BasePermission):
    def has_object_permission(self, request, view, obj):
        # Comprueba cuales son los permisos de edicion del post
        if request.user.is_admin:
            return True
        elif obj.edit_permission == Post.PUBLIC:
            return True
        elif obj.edit_permission == Post.AUTHENTICATED:
            return request.user.is_authenticated
        elif obj.edit_permission == Post.TEAM:
            return request.user.team == obj.author.team
        elif obj.edit_permission == Post.AUTHOR:
            return request.user == obj.author
        else:
            return False
        
class UserHasReadPermission(BasePermission):
    message = "You do not have permission to perform this action."   
    def has_object_permission(self, request, view, obj):
        # Comprueba cuales son los permisos de lectura del post
        if request.user.is_authenticated:
            if request.user.is_admin:
                return True
            if obj.read_permission in ['public', 'authenticated']:
                return True
            if obj.read_permission == 'team':
                return request.user.team == obj.author.team
            if obj.read_permission == 'author':
                return request.user == obj.author
        else:
            # Si el usuario no está autenticado, solo puede leer los posts que tienen read_permission igual a 'public'
            if obj.read_permission == 'public':
                return True

        return False

class PostObjectPermissions(DjangoObjectPermissions):
    # Sobreescribe el método has_object_permission para que se ajuste a los permisos de lectura y edición de los posts
    def has_object_permission(self, request, view, obj):
        # Asegúrate de que obj es una instancia de Post
        if not isinstance(obj, Post):
            return False

        # Comprueba los permisos de lectura si la solicitud es GET
        if request.method == 'GET':
            if obj.read_permission == Post.PUBLIC:
                return True
            elif obj.read_permission == Post.AUTHENTICATED and request.user.is_authenticated:
                return True
            elif obj.read_permission == Post.TEAM and request.user.team == obj.author.team:
                return True
            elif obj.read_permission == Post.AUTHOR and request.user == obj.author:
                return True

        # Comprueba los permisos de edición si la solicitud es PUT, PATCH o DELETE
        elif request.method in ['PUT', 'PATCH', 'DELETE']:
            if obj.edit_permission == Post.PUBLIC:
                return True
            elif obj.edit_permission == Post.AUTHENTICATED and request.user.is_authenticated:
                return True
            elif obj.edit_permission == Post.TEAM and request.user.team == obj.author.team:
                return True
            elif obj.edit_permission == Post.AUTHOR and request.user == obj.author:
                return True

        # Si ninguna de las condiciones anteriores se cumple, el usuario no tiene permiso
        return False

class IsCustomAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin