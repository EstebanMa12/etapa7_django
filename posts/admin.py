from django.contrib import admin

from .models import Post

#Models for posts
@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'edit_permission','write_permission', 'is_deleted')
    list_filter = ('author', 'is_deleted')
    search_fields = ('title', 'author__username')
    list_editable = ('edit_permission','write_permission', 'is_deleted')
    list_per_page = 10
    fieldsets = (
        ('Post', {
            'fields': ('title', 'content', 'author', 'edit_permission','write_permission')
        }),
    )