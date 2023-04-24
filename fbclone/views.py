import random
import json

from django.contrib import messages
from django.contrib.auth import login, authenticate, logout, get_user_model
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm
from django.db.models import Q
from django.views.generic import ListView
from django.shortcuts import render, redirect, get_object_or_404
from .forms import NewUserForm, AvatarForm, PostForm
from .models import Post, CustomUser, FriendRequest, FriendList


def index(request):
    form = AvatarForm(instance=request.user)
    return render(request, "base.html")


def login_page(request):
    if request.method == "POST":
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            user = authenticate(username=username, password=password)
            if user is not None:
                login(request, user)
                messages.info(request, f"You are now logged in as {username}.")
                return redirect('mainpage')
            else:
                messages.error(request, "Invalid username or password.")
        else:
            messages.error(request, "Invalid username or password.")
    form = AuthenticationForm()
    return render(request, "login.html", {"login_form": form})


def register_request(request):
    if request.method == "POST":
        form = NewUserForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request, user)
            messages.success(request, "Registration successful.")
            return redirect('mainpage')
        messages.error(request, "Unsuccessful registration. Invalid information.")
    form = NewUserForm()
    return render(request, "register.html", {"register_form": form})


def messenger(request):
    return render(request, "messenger.html")


def logout_request(request):
    logout(request)
    messages.info(request, "You have successfully logged out.")
    return redirect('mainpage')


def account_management(request):
    if request.method == 'POST':
        form = AvatarForm(request.POST, request.FILES, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('account')
    else:
        form = AvatarForm(instance=request.user)
        return render(request, 'account_manage.html', {'form': form})


def create_post(request):
    if request.user.is_authenticated:
        user = request.user
        try:
            friend_list = FriendList.objects.get(user=user)
            friend_ids = [friend.id for friend in friend_list.friends.all()] + [request.user.id]
            posts = Post.objects.filter(author__id__in=friend_ids).order_by('-pub_date')
            all_friends = friend_list.friends.all()
            not_friends = [person for person in CustomUser.objects.all() if
                           person not in all_friends and person != user]
            suggested_friend = random.choice(not_friends)
        except:
            friend_list = []
            friend_ids = []
            posts = []
            all_friends = []
            suggested_friend = []
    else:
        all_friends = []
        posts = []
        suggested_friend = []
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            author = CustomUser.objects.get(username=request.user.username)
            post.author = author
            post.save()
            return redirect('mainpage')
    else:
        form = PostForm()
    return render(request, 'create_post.html', {'form': form,
                                                'posts': posts,
                                                'all_friends': all_friends,
                                                'suggested_friend': suggested_friend})


@login_required
def friends(request):
    user = request.user
    try:
        friend_list = FriendList.objects.get(user=user)
        all_friends = [friend.username for friend in friend_list.friends.all()]

    except:
        friend_list = []
        all_friends = []
    received_requests = FriendRequest.objects.filter(receiver=request.user, is_active=True)
    sent_requests = FriendRequest.objects.filter(sender=request.user, is_active=True)
    waiting_requests = FriendRequest.objects.filter(receiver=request.user, is_active=False)

    all_users = CustomUser.objects.all()
    return render(request, "friends_list.html", {"friends": friends,
                                                 "all_users": all_users,
                                                 'received_requests': received_requests,
                                                 'sent_requests': sent_requests,
                                                 'waiting_requests': waiting_requests,
                                                 'friend_list': all_friends
                                                 })


def profile(request, user_id):
    User = get_user_model()
    user = get_object_or_404(CustomUser, pk=user_id)
    friend = get_object_or_404(User, id=user_id)
    current_user = request.user
    try:
        friend_list = FriendList.objects.get(user=current_user)
        all_friends = [friend.username for friend in friend_list.friends.all()]
    except:
        friend_list = []
        all_friends = []
    if FriendRequest.objects.filter(sender=current_user, receiver=friend, is_active=True).exists():
        sent = True
    else:
        sent = False
    return render(request, 'profile.html', {'user': user,
                                            'sent': sent,
                                            'friend_list': all_friends})


User = get_user_model()


@login_required
def add_friend(request, user_id):
    user = request.user
    friend = get_object_or_404(User, id=user_id)
    user_friends_list, created = FriendList.objects.get_or_create(user=user)
    friend_friends_list, created = FriendList.objects.get_or_create(user=friend)
    # Sprawdź, czy zaproszenie już zostało wysłane
    if FriendRequest.objects.filter(sender=user, receiver=friend, is_active=True).exists():
        sent = True
        if FriendRequest.objects.filter(sender=user, receiver=friend, is_active=False).exists():
            friend_request = FriendRequest.objects.filter(sender=user,
                                                          receiver=friend).first()  # pobierz pierwszy obiekt pasujący do kryteriów
            if friend_request:
                friend_request.is_active = True
                friend_request.save()  # zapisz zmiany w bazie danych
                messages.error(request, f"Friend request to {friend.username} sent correctly.")
                return redirect('profile', user_id=user_id)
        messages.error(request, f"You've already sent a friend request to {friend.username}")
        return redirect('profile', user_id=user_id)

    # Sprawdź, czy oczekuje już na akceptację zaproszenia
    if FriendRequest.objects.filter(sender=friend, receiver=user, is_active=True).exists():
        messages.error(request, f"{friend.username} already sent you a friend request")
        return redirect('profile', user_id=user_id)

    # Wyślij zaproszenie
    FriendRequest.objects.create(sender=user, receiver=friend)
    messages.success(request, f"You've sent a friend request to {friend.username}")
    return redirect('profile', user_id=user_id)


@login_required
def remove_friend(request, user_id):
    user = request.user
    friend = User.objects.get(id=user_id)
    user_friends_list = FriendList.objects.get(user=user)
    user_friends_list.remove_friend(friend)
    friend_friends_list = FriendList.objects.get(user=friend)
    friend_friends_list.remove_friend(user)
    messages.info(request, "Usunięto znajomego.")
    return redirect('profile', id=user_id)


@login_required
def friend_requests(request):
    return render(request, 'friend_requests.html')


@login_required
def accept_friend_request(request, friend_request_id):
    friend_request = FriendRequest.objects.get(id=friend_request_id)
    friend_request.accept()
    return redirect('friends')


@login_required
def decline_friend_request(request, friend_request_id):
    friend_request = FriendRequest.objects.get(id=friend_request_id)
    friend_request.decline()
    return redirect('friends')


@login_required
def cancel_friend_request(request, friend_request_id):
    friend_request = FriendRequest.objects.get(id=friend_request_id)
    friend_request.cancel()
    messages.success(request, "Friend invitation removed.")
    return redirect('friends')


def user_friends(request, user_id):
    current_user = request.user
    user = get_object_or_404(CustomUser, pk=user_id)
    User = get_user_model()
    if FriendRequest.objects.filter(sender=current_user, receiver=user, is_active=True).exists():
        sent = True
    else:
        sent = False
    try:
        friend_list = FriendList.objects.get(user=user)
        all_friends = friend_list.friends.all()
    except:
        friend_list = []
        all_friends = []
    return render(request, 'user_friends.html', {'all_friends': all_friends,
                                                 'user': user,
                                                 'sent': sent})


def user_timeline(request, user_id):
    current_user = request.user
    user = get_object_or_404(CustomUser, pk=user_id)
    User = get_user_model()
    if FriendRequest.objects.filter(sender=current_user, receiver=user, is_active=True).exists():
        sent = True
    else:
        sent = False
    user = get_object_or_404(CustomUser, pk=user_id)
    posts = Post.objects.filter(author=user).order_by('-pub_date')
    return render(request, 'timeline.html', {'posts': posts,
                                             'user': user,
                                             'sent': sent})


def search_results(request):
    query = request.GET.get('q')
    results = CustomUser.objects.filter(Q(first_name__icontains=query) | Q(last_name__icontains=query))
    return render(request, 'search_results.html', {'results': results})
