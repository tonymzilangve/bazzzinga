
from django.contrib import admin
from .models import Amigos, FriendRequest


class AmigosAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user']
    search_fields = ['user']
    readonly_fields = ['user']

    class Meta:
        model = Amigos


admin.site.register(Amigos, AmigosAdmin)


class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver', 'is_active']
    search_fields = ['sender__username', 'receiver__username']  # sender__email

    class Meta:
        model = FriendRequest


admin.site.register(FriendRequest, FriendRequestAdmin)
