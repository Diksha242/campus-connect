from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

# Extended User Profile
class UserProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='profile')
    bio = models.TextField(blank=True, default='')
    profile_picture = models.ImageField(upload_to='profiles/', blank=True, null=True)
    interests = models.CharField(max_length=500, blank=True)
    year = models.CharField(max_length=20, blank=True, choices=[
        ('1st', '1st Year'),
        ('2nd', '2nd Year'),
        ('3rd', '3rd Year'),
        ('4th', '4th Year'),
    ])
    department = models.CharField(max_length=100, blank=True)
    followers = models.ManyToManyField(User, related_name='following', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)

    def __str__(self):
        return f"{self.user.username}'s Profile"


# Posts/Feed
class Post(models.Model):
    author = models.ForeignKey(User, on_delete=models.CASCADE, related_name='posts')
    title = models.CharField(max_length=200)
    content = models.TextField()
    image = models.ImageField(upload_to='posts/', blank=True, null=True)
    created_at = models.DateTimeField(auto_now_add=True)
    updated_at = models.DateTimeField(auto_now=True)
    likes = models.ManyToManyField(User, related_name='liked_posts', blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


class Comment(models.Model):
    post = models.ForeignKey(Post, on_delete=models.CASCADE, related_name='comments')
    author = models.ForeignKey(User, on_delete=models.CASCADE)
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Comment by {self.author} on {self.post.title}"


# Messaging System
class Message(models.Model):
    sender = models.ForeignKey(User, on_delete=models.CASCADE, related_name='sent_messages')
    receiver = models.ForeignKey(User, on_delete=models.CASCADE, related_name='received_messages')
    content = models.TextField()
    created_at = models.DateTimeField(auto_now_add=True)
    is_read = models.BooleanField(default=False)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Message from {self.sender} to {self.receiver}"


# Events
class Event(models.Model):
    title = models.CharField(max_length=200)
    description = models.TextField()
    organizer = models.ForeignKey(User, on_delete=models.CASCADE, related_name='organized_events')
    image = models.ImageField(upload_to='events/', blank=True, null=True)
    date = models.DateTimeField()
    location = models.CharField(max_length=300)
    capacity = models.IntegerField(default=100)
    attendees = models.ManyToManyField(User, related_name='attending_events', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-date']

    def __str__(self):
        return self.title


# Clubs & Societies
class Club(models.Model):
    name = models.CharField(max_length=200)
    description = models.TextField()
    founder = models.ForeignKey(User, on_delete=models.CASCADE, related_name='founded_clubs')
    image = models.ImageField(upload_to='clubs/', blank=True, null=True)
    members = models.ManyToManyField(User, related_name='clubs', blank=True)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.name


# Marketplace
class MarketplaceItem(models.Model):
    CATEGORY_CHOICES = [
        ('books', 'Books'),
        ('electronics', 'Electronics'),
        ('clothing', 'Clothing'),
        ('furniture', 'Furniture'),
        ('sports', 'Sports Equipment'),
        ('other', 'Other'),
    ]
    
    seller = models.ForeignKey(User, on_delete=models.CASCADE, related_name='marketplace_items')
    title = models.CharField(max_length=200)
    description = models.TextField()
    price = models.DecimalField(max_digits=10, decimal_places=2)
    category = models.CharField(max_length=50, choices=CATEGORY_CHOICES)
    image = models.ImageField(upload_to='marketplace/')
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15, blank=True)
    is_sold = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return self.title


# Lost & Found
class LostFoundItem(models.Model):
    STATUS_CHOICES = [
        ('lost', 'Lost'),
        ('found', 'Found'),
        ('resolved', 'Resolved'),
    ]

    posted_by = models.ForeignKey(User, on_delete=models.CASCADE, related_name='lost_found_items')
    item_name = models.CharField(max_length=200)
    description = models.TextField()
    status = models.CharField(max_length=20, choices=STATUS_CHOICES, default='lost')
    image = models.ImageField(upload_to='lost_found/')
    location = models.CharField(max_length=300)
    date_posted = models.DateTimeField(auto_now_add=True)
    date_occurrence = models.DateField()
    contact_email = models.EmailField()
    contact_phone = models.CharField(max_length=15)

    class Meta:
        ordering = ['-date_posted']

    def __str__(self):
        return f"{self.status.upper()}: {self.item_name}"


# Notifications
class Notification(models.Model):
    NOTIFICATION_TYPES = [
        ('post_like', 'Post Like'),
        ('comment', 'Comment'),
        ('message', 'Message'),
        ('event', 'Event'),
        ('follow', 'Follow'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications')
    notification_type = models.CharField(max_length=50, choices=NOTIFICATION_TYPES)
    actor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='notifications_sent')
    content = models.CharField(max_length=500)
    is_read = models.BooleanField(default=False)
    created_at = models.DateTimeField(auto_now_add=True)
    post = models.ForeignKey(Post, on_delete=models.CASCADE, null=True, blank=True)
    event = models.ForeignKey(Event, on_delete=models.CASCADE, null=True, blank=True)

    class Meta:
        ordering = ['-created_at']

    def __str__(self):
        return f"Notification for {self.user}: {self.notification_type}"
