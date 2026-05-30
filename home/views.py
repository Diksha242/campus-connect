from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.http import JsonResponse
from django.views.decorators.http import require_POST
from django.db.models import Q
from .models import (
    UserProfile, Post, Comment, Message, Event, Club, 
    MarketplaceItem, LostFoundItem, Notification
)

# Auth Views
def index(request):
    if request.user.is_authenticated:
        posts = Post.objects.all()[:20]
        context = {'posts': posts}
        return render(request, 'index.html', context)
    return redirect('login')

def signup(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        email = request.POST.get('email')
        password = request.POST.get('password')
        password2 = request.POST.get('password2')
        
        if password != password2:
            return render(request, 'signup.html', {'error': 'Passwords do not match'})
        
        if User.objects.filter(username=username).exists():
            return render(request, 'signup.html', {'error': 'Username already taken'})
        
        if User.objects.filter(email=email).exists():
            return render(request, 'signup.html', {'error': 'Email already registered'})
        
        user = User.objects.create_user(username=username, email=email, password=password)
        user.save()
        login(request, user)
        return redirect('home')
    
    return render(request, 'signup.html')

def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Invalid username or password'})
    
    return render(request, 'login.html')

def logout_view(request):
    logout(request)
    return redirect('home')

# User Profile
@login_required(login_url='login')
def profile(request, username=None):
    if username:
        user = get_object_or_404(User, username=username)
    else:
        user = request.user
    
    profile = user.profile
    posts = user.posts.all()
    is_following = request.user.profile.followers.filter(id=user.id).exists()
    
    context = {
        'profile_user': user,
        'profile': profile,
        'posts': posts,
        'is_following': is_following,
    }
    return render(request, 'profile.html', context)

@login_required(login_url='login')
def edit_profile(request):
    profile = request.user.profile
    
    if request.method == 'POST':
        profile.bio = request.POST.get('bio', '')
        profile.interests = request.POST.get('interests', '')
        profile.year = request.POST.get('year', '')
        profile.department = request.POST.get('department', '')
        
        if 'profile_picture' in request.FILES:
            profile.profile_picture = request.FILES['profile_picture']
        
        profile.save()
        return redirect('profile', username=request.user.username)
    
    return render(request, 'edit_profile.html', {'profile': profile})

# Posts/Feed
@login_required(login_url='login')
def create_post(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        content = request.POST.get('content')
        image = request.FILES.get('image', None)
        
        post = Post.objects.create(
            author=request.user,
            title=title,
            content=content,
            image=image
        )
        return redirect('home')
    
    return render(request, 'create_post.html')

@login_required(login_url='login')
@require_POST
def like_post(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.user in post.likes.all():
        post.likes.remove(request.user)
        liked = False
    else:
        post.likes.add(request.user)
        liked = True
        
        # Create notification
        if request.user != post.author:
            Notification.objects.create(
                user=post.author,
                notification_type='post_like',
                actor=request.user,
                content=f"{request.user.username} liked your post",
                post=post
            )
    
    return JsonResponse({'liked': liked, 'likes_count': post.likes.count()})

@login_required(login_url='login')
def add_comment(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        comment = Comment.objects.create(
            post=post,
            author=request.user,
            content=content
        )
        
        # Create notification
        if request.user != post.author:
            Notification.objects.create(
                user=post.author,
                notification_type='comment',
                actor=request.user,
                content=f"{request.user.username} commented on your post",
                post=post
            )
        
        return redirect('home')
    
    return redirect('home')

# Messages
@login_required(login_url='login')
def messages(request):
    # Get unique conversations
    conversations = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).values('sender', 'receiver').distinct()
    
    message_list = Message.objects.filter(
        Q(sender=request.user) | Q(receiver=request.user)
    ).order_by('-created_at')
    
    context = {
        'messages': message_list,
    }
    return render(request, 'messages.html', context)

@login_required(login_url='login')
def chat(request, username):
    other_user = get_object_or_404(User, username=username)
    
    if request.method == 'POST':
        content = request.POST.get('content')
        Message.objects.create(
            sender=request.user,
            receiver=other_user,
            content=content
        )
        return redirect('chat', username=username)
    
    # Get conversation
    conversation = Message.objects.filter(
        Q(sender=request.user, receiver=other_user) |
        Q(sender=other_user, receiver=request.user)
    ).order_by('created_at')
    
    # Mark as read
    Message.objects.filter(sender=other_user, receiver=request.user).update(is_read=True)
    
    context = {
        'other_user': other_user,
        'messages': conversation,
    }
    return render(request, 'chat.html', context)

# Notifications
@login_required(login_url='login')
def notifications(request):
    notifs = request.user.notifications.all()
    notifs.update(is_read=True)
    
    context = {'notifications': notifs}
    return render(request, 'notifications.html', context)

# Events
@login_required(login_url='login')
def events(request):
    all_events = Event.objects.all()
    
    context = {'events': all_events}
    return render(request, 'events.html', context)

@login_required(login_url='login')
def create_event(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        date = request.POST.get('date')
        location = request.POST.get('location')
        capacity = request.POST.get('capacity', 100)
        image = request.FILES.get('image', None)
        
        event = Event.objects.create(
            title=title,
            description=description,
            organizer=request.user,
            date=date,
            location=location,
            capacity=capacity,
            image=image
        )
        return redirect('events')
    
    return render(request, 'create_event.html')

@login_required(login_url='login')
def event_detail(request, event_id):
    event = get_object_or_404(Event, id=event_id)
    is_attending = request.user in event.attendees.all()
    
    if request.method == 'POST':
        if is_attending:
            event.attendees.remove(request.user)
        else:
            event.attendees.add(request.user)
            
            # Create notification
            if request.user != event.organizer:
                Notification.objects.create(
                    user=event.organizer,
                    notification_type='event',
                    actor=request.user,
                    content=f"{request.user.username} joined your event",
                    event=event
                )
        
        return redirect('event_detail', event_id=event_id)
    
    context = {
        'event': event,
        'is_attending': is_attending,
    }
    return render(request, 'event_detail.html', context)

# Clubs
@login_required(login_url='login')
def clubs(request):
    all_clubs = Club.objects.all()
    
    context = {'clubs': all_clubs}
    return render(request, 'clubs.html', context)

@login_required(login_url='login')
def create_club(request):
    if request.method == 'POST':
        name = request.POST.get('name')
        description = request.POST.get('description')
        image = request.FILES.get('image', None)
        
        club = Club.objects.create(
            name=name,
            description=description,
            founder=request.user,
            image=image
        )
        club.members.add(request.user)
        return redirect('clubs')
    
    return render(request, 'create_club.html')

@login_required(login_url='login')
def club_detail(request, club_id):
    club = get_object_or_404(Club, id=club_id)
    is_member = request.user in club.members.all()
    
    if request.method == 'POST':
        if is_member:
            club.members.remove(request.user)
        else:
            club.members.add(request.user)
        
        return redirect('club_detail', club_id=club_id)
    
    context = {
        'club': club,
        'is_member': is_member,
    }
    return render(request, 'club_detail.html', context)

# Marketplace
@login_required(login_url='login')
def marketplace(request):
    items = MarketplaceItem.objects.filter(is_sold=False)
    
    context = {'items': items}
    return render(request, 'marketplace.html', context)

@login_required(login_url='login')
def create_listing(request):
    if request.method == 'POST':
        title = request.POST.get('title')
        description = request.POST.get('description')
        price = request.POST.get('price')
        category = request.POST.get('category')
        image = request.FILES.get('image')
        contact_email = request.POST.get('contact_email')
        contact_phone = request.POST.get('contact_phone')
        
        MarketplaceItem.objects.create(
            seller=request.user,
            title=title,
            description=description,
            price=price,
            category=category,
            image=image,
            contact_email=contact_email,
            contact_phone=contact_phone
        )
        return redirect('marketplace')
    
    context = {'categories': MarketplaceItem.CATEGORY_CHOICES}
    return render(request, 'create_listing.html', context)

@login_required(login_url='login')
def item_detail(request, item_id):
    item = get_object_or_404(MarketplaceItem, id=item_id)
    
    context = {'item': item}
    return render(request, 'item_detail.html', context)

# Lost & Found
@login_required(login_url='login')
def lostfound(request):
    items = LostFoundItem.objects.filter(status__in=['lost', 'found'])
    
    context = {'items': items}
    return render(request, 'lostfound.html', context)

@login_required(login_url='login')
def create_lost_found(request):
    if request.method == 'POST':
        item_name = request.POST.get('item_name')
        description = request.POST.get('description')
        status = request.POST.get('status')
        image = request.FILES.get('image')
        location = request.POST.get('location')
        date_occurrence = request.POST.get('date_occurrence')
        contact_email = request.POST.get('contact_email')
        contact_phone = request.POST.get('contact_phone')
        
        LostFoundItem.objects.create(
            posted_by=request.user,
            item_name=item_name,
            description=description,
            status=status,
            image=image,
            location=location,
            date_occurrence=date_occurrence,
            contact_email=contact_email,
            contact_phone=contact_phone
        )
        return redirect('lostfound')
    
    context = {'statuses': LostFoundItem.STATUS_CHOICES}
    return render(request, 'create_lost_found.html', context)

# Resources/Student Voice
@login_required(login_url='login')
def resources(request):
    posts = Post.objects.filter(title__icontains='resource')
    
    context = {'posts': posts}
    return render(request, 'resources.html', context)

@login_required(login_url='login')
def student_voice(request):
    posts = Post.objects.all()
    
    context = {'posts': posts}
    return render(request, 'student_voice.html', context)