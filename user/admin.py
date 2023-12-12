from typing import Any
from django.contrib import admin
from django.http.request import HttpRequest
from .models import Post

#Models for posts
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'permission', 'is_deleted')
    list_filter = ('author', 'permission', 'is_deleted')
    search_fields = ('title', 'author__username', 'permission')
    ordering = ('title', 'author', 'permission', 'is_deleted')
    list_editable = ('permission', 'is_deleted')
    list_per_page = 10
    fieldsets = (
        ('Post', {
            'fields': ('title', 'content', 'author', 'permission')
        }),
    )


#Models for teams
from .models import Team
@admin.register(Team)
class TeamAdmin(admin.ModelAdmin):
    list_display = ('team_name',)
    list_filter = ('team_name',)
    search_fields = ('team_name',)
    ordering = ('team_name',)
    list_per_page = 10
    fieldsets = (
        (None, {
            'fields': ('team_name',)
        }),
    )
    
    

#Models for users
from .models import CustomUser
from django.contrib.auth.forms import (
    AdminPasswordChangeForm,
    UserChangeForm,
    UserCreationForm,
)
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id','username', 'team', 'is_superuser', 'is_staff', 'is_active')
    list_filter = ('username', 'team', 'is_superuser', 'is_staff', 'is_active')
    list_display_links = ('id', 'username')
    search_fields = ('username', 'team__team_name')
    ordering = ('username', 'team', 'is_superuser', 'is_staff', 'is_active')
    list_per_page = 10
    fieldsets = (
        (None, {
            'fields': ('username','password','team', 'is_superuser', 'is_staff', 'is_active')
        }),
    )
    change_password_form = AdminPasswordChangeForm
    

# class UserAdmin(BaseUserAdmin):
#     list_display = ('username',
#                     'team',
#                     'is_superuser',
#                     'is_staff',
#                     'is_active')
    
#     def get_fieldsets(self, request, obj: None) :
#         fieldsets = super().get_fieldsets(request, obj)
#         if obj is not None:
#             fieldsets = (
#                 (None, {'fields': ('username',
#                                 'password',
#                                 'team',
#                                 'is_superuser',
#                                 'is_staff',
#                                 'is_active')}),
#             )
#         return fieldsets