from django.contrib import admin
from .models import Category, Tag, Post, Comment, Like, SavedPost

@admin.register(Category)
class CategoryAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Tag)
class TagAdmin(admin.ModelAdmin):
    list_display = ('name', 'slug')
    search_fields = ('name',)
    prepopulated_fields = {'slug': ('name',)}

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ('title', 'author', 'status', 'created_at', 'updated_at')
    list_filter = ('status', 'created_at', 'categories', 'tags')
    search_fields = ('title', 'content')
    prepopulated_fields = {'slug': ('title',)}
    filter_horizontal = ('categories', 'tags')
    date_hierarchy = 'created_at'
    
    def get_queryset(self, request):
        qs = super().get_queryset(request)
        if request.user.is_superuser or request.user.is_admin_role():
            return qs
        return qs.filter(author=request.user)

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'parent', 'created_at')
    list_filter = ('created_at',)
    search_fields = ('text', 'user__username', 'post__title')
    date_hierarchy = 'created_at'

@admin.register(Like)
class LikeAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'comment')
    list_filter = ('post', 'comment')

@admin.register(SavedPost)
class SavedPostAdmin(admin.ModelAdmin):
    list_display = ('user', 'post', 'saved_at')
    list_filter = ('saved_at',)
    search_fields = ('user__username', 'post__title')
