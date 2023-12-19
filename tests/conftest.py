import pytest
from pytest_factoryboy import register

from .factories import UserFactory, PostFactory, LikesFactory, CommentsFactory

register(UserFactory)
register(PostFactory)
register(LikesFactory)
register(CommentsFactory)


# @pytest.fixture()
# def user(db, django_user_model):
#     return django_user_model.objects.create_user(
#         username='testuser',
#         password='password',
#         team='team1',
#         is_superuser=False,
#         is_admin=False,
#     )

import os
import django
from django.conf import settings

# Set the DJANGO_SETTINGS_MODULE environment variable.
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'avanzatech_blog.settings')

# Configure Django settings.
django.setup()
