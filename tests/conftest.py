import os
import django
from django.conf import settings

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avanzatech_blog.settings')

# Configure Django settings.
django.setup()

pytest_plugins = [
    "django",
]


from pytest_factoryboy import register

from .factories import UserFactory, PostFactory, LikesFactory, CommentsFactory

register(UserFactory)
register(PostFactory)
register(LikesFactory)
register(CommentsFactory)
