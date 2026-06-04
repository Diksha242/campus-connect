"""
URL configuration for campus_connect project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='home'),
    
    path('signup/', views.signup, name='signup'),
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),

    # Profile
    path('profile/', views.profile, name='profile'),
    path('profile/edit/', views.edit_profile, name='edit_profile'),
    path('profile/<str:username>/follow/', views.follow_user, name='follow_user'),
    path('profile/<str:username>/followers/', views.followers, name='profile_followers'),
    path('profile/<str:username>/following/', views.following, name='profile_following'),
    path('profile/<str:username>/', views.profile, name='user_profile'),
    path('post/<int:post_id>/delete/', views.delete_post, name='delete_post'),
    path('discover-people/', views.discover_people, name='discover_people'),

    # Posts
    path('create-post/', views.create_post, name='create_post'),
    path('like-post/<int:post_id>/', views.like_post, name='like_post'),
    path('add-comment/<int:post_id>/', views.add_comment, name='add_comment'),

    # Messages
    path('messages/', views.messages, name='messages'),
    path('chat/<str:username>/', views.chat, name='chat'),

    # Notifications
    path('notifications/', views.notifications, name='notifications'),

    # Events
    path('events/', views.events, name='events'),
    path('create-event/', views.create_event, name='create_event'),
    path('event/<int:event_id>/', views.event_detail, name='event_detail'),

    # Clubs
    path('clubs/', views.clubs, name='clubs'),
    path('create-club/', views.create_club, name='create_club'),
    path('club/<int:club_id>/', views.club_detail, name='club_detail'),

    # Marketplace
    path('marketplace/', views.marketplace, name='marketplace'),
    path('create-listing/', views.create_listing, name='create_listing'),
    path('item/<int:item_id>/', views.item_detail, name='item_detail'),

    # Lost & Found
    path('lostfound/', views.lostfound, name='lostfound'),
    path('create-lost-found/', views.create_lost_found, name='create_lost_found'),

    # Resources & Student Voice
    path('resources/', views.resources, name='resources'),
    path('student-voice/', views.student_voice, name='student_voice'),
]
