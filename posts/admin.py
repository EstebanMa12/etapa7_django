from django.contrib import admin

from .models import Post, Like, Comment

class LikeInline(admin.TabularInline):
    model = Like
    extra = 1

class CommentInline(admin.TabularInline):
    model = Comment
    extra = 1
#Models for posts
class PostAdmin(admin.ModelAdmin):
    list_display = ('id','title', 'author', 'edit_permission','read_permission', 'is_deleted')
    list_filter = ('id','author', 'is_deleted')
    search_fields = ('title', 'author__username')
    list_editable = ('edit_permission','read_permission', 'is_deleted')
    list_per_page = 10
    fieldsets = (
        ('Post', {
            'fields': ('title', 'content', 'author', 'edit_permission','read_permission')
        }),
    )
    inlines = [LikeInline, CommentInline]


admin.site.register(Post, PostAdmin)
admin.site.register(Like)
admin.site.register(Comment)    