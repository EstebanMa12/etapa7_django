from rest_framework.permissions import BasePermission, DjangoObjectPermissions
from posts.models import Post
class UserHasEditPermission(BasePermission):
    """
    Custom permission class to check if a user has edit permission for a post.
    """
    message = "You do not have permission to perform this action."
    def has_object_permission(self, request, view, obj):
        """
        Check if the user has edit permission for the given post object.

        Args:
            request (HttpRequest): The request object.
            view (View): The view object.
            obj (Post): The post object.

        Returns:
            bool: True if the user has edit permission, False otherwise.
        """
        if request.user.is_authenticated:
            # Check the edit permissions of the post
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
            # If the user is not authenticated, they can edit posts with 'public' edit permission
            if obj.edit_permission == Post.PUBLIC:
                return True
            
        return False
        
class UserHasReadPermission(BasePermission):
    """
    Custom permission class to check if a user has read permission for an object.

    This permission class checks if the user is authenticated and has the necessary permissions
    to read the object. It considers different scenarios based on the read_permission attribute
    of the object and the user's role.

    Attributes:
        message (str): The error message to be displayed when the user does not have permission.
    """

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


class IsCustomAdminUser(BasePermission):
    """
    Allows access only to admin users.
    """
    def has_permission(self, request, view):
        return request.user.is_authenticated and request.user.is_admin