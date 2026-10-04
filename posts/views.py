from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404 
from django.shortcuts import render, redirect
from .forms import PostForm
# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request, 'posts/home.html', {'posts': posts})
def post_detail(request, id):
    post = get_object_or_404(Post , id = id)
    return render(request , 'posts/post_detail.html', {'post': post})
def  post_create(request):
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('home')
    else:
        form = PostForm()
    return render(request, 'posts/post_form.html', {'form': form})
def post_edit(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        form = PostForm(request.POST, instance=post)
        if form.is_valid():
            form.save()
            return redirect('post_detail', id=post.id)
    else:
        form = PostForm(instance=post)
    return render(request, 'posts/post_form.html', {'form': form})

def post_delete(request, id):
    post = get_object_or_404(Post, id=id)
    if request.method == 'POST':
        post.delete()
        return redirect('home')
    return render(request, 'posts/post_confirm_delete.html', {'post': post})
