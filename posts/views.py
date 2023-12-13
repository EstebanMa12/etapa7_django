
# POSTS
from rest_framework import status
from rest_framework import generics
from rest_framework.response import Response
from rest_framework.permissions import IsAuthenticated
from posts.models import Post
from posts.serializers import PostSerializer
from django.core.exceptions import ValidationError
from .permissions import UserHasEditPermission, UserHasReadPermission
from rest_framework.pagination import PageNumberPagination


# View for create POST and List
class PostCreateView(generics.ListCreateAPIView):
    queryset = Post.objects.all()
    serializer_class = PostSerializer
    pagination_class = PageNumberPagination
    
    def get_permissions(self):
        permissions = []
        if self.request.method == 'POST':
            permissions.append(IsAuthenticated)
            # self.permission_classes = [IsAuthenticated,]
        else:
            permissions.append(UserHasReadPermission)
            # self.permission_classes = [UserHasReadPermission,]
        return [p() for p in permissions]      
    
    def perform_create(self, serializer):
        try:
            serializer.save(author=self.request.user)
        except ValidationError as e:
            return Response({"error": str(e)}, status=status.HTTP_400_BAD_REQUEST)
    
    def get_queryset(self):
        queryset = Post.objects.all()
        
        # Filtrado
        for post in list(queryset):
            object_permissions  = UserHasReadPermission()
            if not object_permissions.has_object_permission(self.request, self, post):
                queryset = queryset.exclude(id=post.id)
        return queryset
    # def get(self, request, *args, **kwargs): 
    #     self.check_permissions(request)   
    #     # Aplica el filtrado, la ordenación y la paginación a la consulta    
    #     posts = self.filter_queryset(self.get_queryset())
    #     # Ahora, 'posts' solo incluirá los posts que el usuario tiene permiso para ver
    #     serializer = PostSerializer(posts, many=True)
    #     return Response(serializer.data)

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

