from django.contrib.auth.models import Permission
from django.contrib.contenttypes.models import ContentType

class AutoReadPermissionMiddleware:
    """
    Middleware class that automatically grants read permission to users who have edit permission on posts.
    """
    def __init__(self, get_response):
        self.get_response = get_response
        
    def __call__(self, request):
        content_type = ContentType.objects.get(
            app_label='posts',
            model='post')
        edit_permission = Permission.objects.get(content_type = content_type,
                                                codename='change_post')
        if edit_permission in request.user.user_permissions.all():
            
            # User has the 'edit' permission on posts - give them read access too.
            read_permission = Permission.objects.get(content_type = content_type,
                                                codename='view_post')
            if read_permission not in request.user.user_permissions.all():
                request.user.user_permissions.add(read_permission)
                request.user.save()
                
        return self.get_response(request)
    