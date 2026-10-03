from django.shortcuts import render
from .models import Post
from django.shortcuts import get_object_or_404 
from django.shortcuts import render, redirect
# Create your views here.
def home(request):
    posts = Post.objects.all()
    return render(request, 'home.html', {'posts': posts})
def post_detail(request, id):
    post = get_object_or_404(Post , id = id)
    return render(request , 'post_detail.html', {'post': post})
