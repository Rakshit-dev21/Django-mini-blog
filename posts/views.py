from django.contrib.auth import logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.shortcuts import get_object_or_404, redirect, render
from rest_framework_simplejwt.exceptions import TokenError
from rest_framework_simplejwt.tokens import RefreshToken

from .forms import PostForm
from .jwt_auth import REFRESH_COOKIE, clear_jwt_cookies, set_jwt_cookies
from .models import Post


def register_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            return set_jwt_cookies(redirect('home'), user)
    else:
        form = UserCreationForm()
    return render(request, 'registration/register.html', {'form': form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if request.method == 'POST':
        form = AuthenticationForm(request, data=request.POST)
        if form.is_valid():
            user = form.get_user()
            return set_jwt_cookies(redirect('home'), user)
    else:
        form = AuthenticationForm()
    return render(request, 'registration/login.html', {'form': form})


@login_required(login_url='login')
def home(request):
    posts = Post.objects.filter(author=request.user).order_by('-created_at')
    return render(request, 'posts/home.html', {'posts': posts, 'heading': 'My Posts'})


def post_detail(request, id):
    post = get_object_or_404(Post, id=id)
    return render(request, 'posts/post_detail.html', {'post': post})


@login_required(login_url='login')
def post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})


@login_required(login_url='login')
def post_edit(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form})


@login_required(login_url='login')
def post_delete(request, id):
    post = get_object_or_404(Post, id=id, author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})


@login_required(login_url='login')
def logout_view(request):
    raw_refresh = request.COOKIES.get(REFRESH_COOKIE)
    if raw_refresh:
        try:
            RefreshToken(raw_refresh).blacklist()
        except TokenError:
            pass
    logout(request)
    return clear_jwt_cookies(redirect('login'))


@login_required(login_url='login')
def all_posts(request):
    posts = Post.objects.select_related('author').order_by('-created_at')
    return render(request, 'posts/home.html', {'posts': posts, 'heading': 'All Posts'})