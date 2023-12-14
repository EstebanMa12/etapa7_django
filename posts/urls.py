from django.urls import path
from .views import PostCreateView, PostEditView, PostDetailView


urlpatterns = [
    path('post/', PostCreateView.as_view(), name='post-create'),
    path('post/<int:id>', PostDetailView.as_view(), name='post'),
    path('blog/<int:id>', PostEditView.as_view(), name='post-edit'),
    
    # path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    # path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    # path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
]