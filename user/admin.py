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
from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
@admin.register(CustomUser)
class CustomUserAdmin(admin.ModelAdmin):
    list_display = ('id','email', 'team', 'is_superuser', 'is_staff', 'is_active')
    list_filter = ('email', 'team', 'is_superuser', 'is_staff', 'is_active')
    list_display_links = ('id', 'email')
    search_fields = ('email', 'team__team_name')
    ordering = ('email', 'team', 'is_superuser', 'is_staff', 'is_active')
    list_per_page = 10
    fieldsets = (
        (None, {
            'fields': ('email', 'team', 'is_superuser', 'is_staff', 'is_active')
        }),
    )
    

class UserAdmin(BaseUserAdmin):
    list_display = ('email',
                    'team',
                    'is_superuser',
                    'is_staff',
                    'is_active')
    
    def get_fieldsets(self, request, obj: None) :
        fieldsets = super().get_fieldsets(request, obj)
        if obj is not None:
            fieldsets = (
                (None, {'fields': ('username','password')}),
                
            )
        return fieldsets
    
    
admin.site.unregister(CustomUser)
admin.site.register(CustomUser, UserAdmin)