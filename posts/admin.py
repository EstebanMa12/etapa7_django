from django.contrib import admin

from .models import Post
from comments.models import Comment
from likes.models import Like
from rest_framework.pagination import PageNumberPagination

class LikeInline(admin.TabularInline):
    model = Like
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
#Models for posts
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'author', 'edit_permission','read_permission')
    list_filter = ('id','author')
    search_fields = ('title', 'author__username')
    list_editable = ('edit_permission','read_permission')
    list_per_page = 10
    fieldsets = (
        ('Post', {
            'fields': ('title', 'content', 'author', 'edit_permission','read_permission')
        }),
    )
    list_display_links = ('id', 'title')
    inlines = [LikeInline, CommentInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Comment)    