 
from django.contrib import admin
from django.urls import include, path
from rest_framework.documentation import include_docs_urls


urlpatterns = [
    path('admin/', admin.site.urls),
    path('user/', include('user.urls')),
    path('', include('posts.urls')),
    path('likes/', include('likes.urls'), name='like-list'),
    path('comments/', include('comments.urls')),
    path('docs/', include_docs_urls(title='Avanzatech Blog Documentation')),
]

"""
URL patterns for the Avanzatech Blog application.

Includes the following patterns:
- 'admin/' for the Django admin site
- 'user/' for user-related URLs
- '' for post-related URLs
- 'likes/' for like-related URLs
- 'comments/' for comment-related URLs
- 'docs/' for the Avanzatech Blog documentation

"""
