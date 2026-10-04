from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404 
from django.shortcuts import render, redirect
from .forms import PostForm
from django.contrib.auth.forms import UserCreationForm , AuthenticationForm
from django.contrib.auth import login , logout
from django.contrib.auth.decorators import login_required
# Create your views here.
def register_view(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            login(request , user)
            return redirect('home')
    else:
        initial_data = {'username': '', 'password1': '', 'password2': ''}
        form = UserCreationForm(initial=initial_data)
    return render(request , 'registration/register.html' , {'form' : form})


def login_view(request):
    if request.user.is_authenticated:
        return redirect('home')
    if(request.method == 'POST'):
        form = AuthenticationForm(request , data = request.POST)
        if(form.is_valid()):
            user = form.get_user()
            login(request , user)
            return redirect('home')
    else:
        intial_data = {'username': '', 'password': ''}
        form = AuthenticationForm(initial = intial_data)
    return render(request , 'registration/login.html' , {'form' : form}) 

@login_required(login_url='login')
def home(request):
    posts = Post.objects.filter(author = request.user)
    return render(request, 'posts/home.html', {'posts': posts})

def post_detail(request, id):
    post = get_object_or_404(Post , id = id)
    return render(request , 'posts/post_detail.html', {'post': post})

@login_required(login_url='login')
def  post_create(request):
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
    post = get_object_or_404(Post, id=id , author=request.user)
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
    post = get_object_or_404(Post, id=id , author=request.user)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})

@login_required(login_url='login')
def logout_view(request):
    logout(request)
    return redirect('login')

@login_required(login_url='login')
def all_posts(request):
    posts = Post.objects.all()
    return render(request, 'posts/home.html', {'posts': posts , 'heading' : 'All Posts'})