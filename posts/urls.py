from django.urls import path
from . import views


urlpatterns = [
    path('post/', views.PostCreateView.as_view(), name='post-create'),
    # path('post/<int:pk>/', views.PostDetailView.as_view(), name='post-detail'),
    # path('post/<int:pk>/edit/', views.PostUpdateView.as_view(), name='post-update'),
    # path('post/<int:pk>/delete/', views.PostDeleteView.as_view(), name='post-delete'),
    
]