from django.contrib import admin

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