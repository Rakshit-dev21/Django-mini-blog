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