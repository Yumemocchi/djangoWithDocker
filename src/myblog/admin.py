from django.contrib import admin
from .models import PostBlog, Category, Comment

# admin.site.register(Category)


@admin.register(Category)
class BlogCategories(admin.ModelAdmin):
    pass


@admin.register(PostBlog)
class BlogPostAdmin(admin.ModelAdmin):
    list_display = (
        'title',
        'created_date_post',
        'total_likes',
        'author'
    )

    # list_editable = ('title',)
    # list_display_links = ('author',)
    search_fields = ('title',)
    list_filter = ('author',)


@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    pass
