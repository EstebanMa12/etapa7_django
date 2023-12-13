from rest_framework.permissions import IsAuthenticated, BasePermission
from .models import Post
class UserHasEditPermission(BasePermission):
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
        
class UserHasReadPermission(BasePermission):
    def has_permission(self, request, view):
        # comprueba los permisos de lectura del user
        return request.user.is_authenticated
        
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
