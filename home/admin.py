from django.contrib import admin
from .models import (
    UserProfile, Post, Comment, Message, Event, Club,
    MarketplaceItem, LostFoundItem, Notification
)

@admin.register(UserProfile)
class UserProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'department', 'year', 'created_at']
    search_fields = ['user__username', 'department']

@admin.register(Post)
class PostAdmin(admin.ModelAdmin):
    list_display = ['title', 'author', 'created_at']
    search_fields = ['title', 'author__username']
    readonly_fields = ['created_at', 'updated_at']

@admin.register(Comment)
class CommentAdmin(admin.ModelAdmin):
    list_display = ['post', 'author', 'created_at']
    search_fields = ['post__title', 'author__username']

@admin.register(Message)
class MessageAdmin(admin.ModelAdmin):
    list_display = ['sender', 'receiver', 'created_at', 'is_read']
    search_fields = ['sender__username', 'receiver__username']

@admin.register(Event)
class EventAdmin(admin.ModelAdmin):
    list_display = ['title', 'organizer', 'date', 'location']
    search_fields = ['title', 'organizer__username']

@admin.register(Club)
class ClubAdmin(admin.ModelAdmin):
    list_display = ['name', 'founder', 'created_at']
    search_fields = ['name', 'founder__username']

@admin.register(MarketplaceItem)
class MarketplaceItemAdmin(admin.ModelAdmin):
    list_display = ['title', 'seller', 'price', 'category', 'is_sold']
    search_fields = ['title', 'seller__username']
    list_filter = ['category', 'is_sold']

@admin.register(LostFoundItem)
class LostFoundItemAdmin(admin.ModelAdmin):
    list_display = ['item_name', 'posted_by', 'status', 'date_posted']
    search_fields = ['item_name', 'posted_by__username']
    list_filter = ['status']

@admin.register(Notification)
class NotificationAdmin(admin.ModelAdmin):
    list_display = ['user', 'notification_type', 'actor', 'is_read', 'created_at']
    search_fields = ['user__username', 'actor__username']
    list_filter = ['notification_type', 'is_read']
