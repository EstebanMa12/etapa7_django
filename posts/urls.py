from django.urls import path
from comments.views import CommentCreateView
from .views import PostCreateView, PostEditView, PostDetailView
from likes.views import LikeCreateView


urlpatterns = [
    path('post/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:id>', PostDetailView.as_view(), name='post'),
    path('blog/<int:id>', PostEditView.as_view(), name='post-edit'),
    path('post/<int:post_id>/like/', LikeCreateView.as_view(), name='like-create-delete'),
    path('post/<int:post_id>/comment', CommentCreateView.as_view(), name='comment-create-delete')
    # path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    # path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    # path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
]