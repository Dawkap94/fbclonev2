from django.contrib import admin
from .models import CustomUser, Post, FriendList, FriendRequest, Comment, Messages, Like

# Register your models here.

admin.site.register(CustomUser)
admin.site.register(Post)


class FriendListAdmin(admin.ModelAdmin):
    list_filter = ['user']
    list_display = ['user', 'display_friends']
    search_fields = ['user__username']
    readonly_fields = ['user']

    def display_friends(self, obj):
        return ", ".join([str(friend) for friend in obj.friends.all()])

    display_friends.short_description = 'Friends'

    class Meta:
        model = FriendList


admin.site.register(FriendList, FriendListAdmin)


class FriendRequestAdmin(admin.ModelAdmin):
    list_filter = ['sender', 'receiver']
    list_display = ['sender', 'receiver']
    search_fields = ['sender__username', 'receiver__username']

    class Meta:
        model = FriendRequest


admin.site.register(FriendRequest, FriendRequestAdmin)

admin.site.register(Comment)
admin.site.register(Messages)
admin.site.register(Like)