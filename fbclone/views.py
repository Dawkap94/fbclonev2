from django.contrib import messages
from django.contrib.auth import login, authenticate, logout
from django.contrib.auth.forms import AuthenticationForm
from django.http import HttpResponse
from django.shortcuts import render, redirect, get_object_or_404
from django.utils import timezone

from .forms import NewUserForm, AvatarForm, PostForm, EditUserInfoForm
from .models import Post, CustomUser


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
    posts = Post.objects.filter(author=request.user.id)
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
                                                'posts': posts})


def friends(request):
    user = CustomUser.objects.get(id=request.user.id)
    all_users = CustomUser.objects.all()
    friends = user.friends.all()
    return render(request, "friends_list.html", {"friends": friends,
                                                 "all_users": all_users})


def profile(request, user_id):
    user = get_object_or_404(CustomUser, pk=user_id)
    return render(request, 'profile.html', {'user': user})
