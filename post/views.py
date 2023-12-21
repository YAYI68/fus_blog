from django.shortcuts import render, redirect
from django.urls import reverse
from django.http import HttpResponse
from django.contrib.auth.decorators import login_required
from django.views import View
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth import login
from .forms import PostForm
from .models import Post
# Create your views here.


class RegisterView(View):
    def get(self, request):
        form = UserCreationForm()
        return render(request, 'user/signup.html', {'form': form})

    def post(self, request):
        form = UserCreationForm(request.POST)
        if form.is_valid():
            user = form.save()
            print(user)
            # login(request, user)
            return redirect('login')
        else:
            return render(request, 'user/signup.html', {'form': form})


def index(request):
    # context = {}
    posts = Post.objects.all().order_by('-created_at')

    print(posts)
    return render(request, "post/index.html", context={'posts': posts})


def detail(request, id):
    try:
        post = Post.objects.get(id=id)
        return render(request, "post/post_detail.html", context={'post': post})
    except:
        return HttpResponse(status=405)


@login_required()
def create(request):
    form = PostForm()
    try:
        user = request.user
        form = PostForm()
        if request.method == "POST":
            title = request.POST.get("title")
            content = request.POST.get("content")
            form = PostForm(data={"title": title, "content": content})
            if form.is_valid():
                post = form.save(commit=False)
                post.author = user
                post.save()
                return redirect("index")
        else:
            return render(request, 'post/create_post.html', context={'form': form})
    except:
        return render(request, 'post/create_post.html', context={'form': form})


@login_required()
def update(request, id):
    try:
        user = request.user
        post = Post.objects.get(id=id)
        if user != post.author:
            return redirect("index")
        if request.method == "POST":
            title = request.POST.get("title")
            content = request.POST.get("content")
            form = PostForm(instance=post, data={
                            "title": title, "content": content})
            if form.is_valid():
                post = form.save()
                return redirect(reverse('post_detail', args=[post.id]))
        else:
            form = PostForm(instance=post)
            return render(request, 'post/edit_post.html', context={'form': form, "post": post})
    except:
        return HttpResponse(status=500)


@login_required()
def delete(request, id):
    try:
        user = request.user
        post = Post.objects.get(id=id)
        if user != post.author:
            return redirect("index")
        if request.method == "POST":
            post.delete()
            return redirect("index")
        else:
            return render(request, "post/delete_post.html", context={"post": post})
    except:
        return HttpResponse(status=500)
