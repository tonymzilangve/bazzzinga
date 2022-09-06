from django.contrib import admin
from .models import *


class ProfileAdmin(admin.ModelAdmin):
    list_display = ('id', 'nick', 'gender', 'avatar')
    list_display_links = ('id', 'nick')
    search_fields = ('nick',)
    list_filter = ('gender',)


admin.site.register(Profile, ProfileAdmin)


class PostAdmin(admin.ModelAdmin):
    list_display = ('author', 'datetime', 'text')
    list_display_links = ('author',)
    search_fields = ('author',)
    list_filter = ('author',)


admin.site.register(Post, PostAdmin)


class CommentAdmin(admin.ModelAdmin):
    list_display = ('datetime', 'author', 'text', 'post_id')
    list_display_links = ('author',)
    search_fields = ('author',)
    list_filter = ('author',)


admin.site.register(Comment, CommentAdmin)