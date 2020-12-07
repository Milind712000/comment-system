from django.contrib import admin
from .models import Post, Comment


class CommentInline(admin.TabularInline):
    model = Comment
    fields = ["comment_text"]
    extra = 0


class PostAdmin(admin.ModelAdmin):
    inlines = [CommentInline]


admin.site.register(Comment)
admin.site.register(Post, PostAdmin)
