from rest_framework.permissions import BasePermission
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
        
class IsCustomAdminUser(BasePermission):
    def has_permission(self, request, view):
        return bool(request.user.is_authenticated and request.user.is_admin)
