from django.urls import path
from .views import LikeListView
urlpatterns = [
    path('', LikeListView.as_view(), name='like-list'),
]