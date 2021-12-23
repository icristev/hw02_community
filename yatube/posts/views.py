from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from yatube.settings import POSTS_ON_INDEX

from .forms import PostForm
from .models import Group, Post


def get_page(request, post_list):
    paginator = Paginator(post_list, POSTS_ON_INDEX)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    return page_obj


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all()

    context = {
        'page_obj': get_page(request, posts),
    }

    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()

    context = {
        'group': group,
        'posts': posts,
        'page_obj': get_page(request, posts),
    }

    return render(request, template, context)


def profile(request, username):
    template = 'posts/profile.html'
    author = get_object_or_404(User, username=username)
    posts = author.posts.all()
    number_of_posts = posts.count()
    context = {
        'page_obj': get_page(request, posts),
        'author': author,
        'posts': posts,
        'number_of_posts': number_of_posts,
    }
    return render(request, template, context)


def post_detail(request, post_id):
    template = 'posts/post_detail.html'
    post = get_object_or_404(Post, id=post_id)
    author = post.author
    count = author.posts.all().count()
    context = {'post': post, 'post_count': count}

    return render(request, template, context)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    if request.method == 'POST':
        form = PostForm(request.POST or None)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('posts:profile', request.user)
        return render(request, template, {'form': form})
    form = PostForm()
    is_edit = True
    context = {'form': form,
               'is_edit': is_edit}
    return render(request, template, context)


@login_required
def post_edit(request, post_id):
    post = get_object_or_404(Post, id=post_id)
    form = PostForm(instance=post)
    if request.method == 'POST':
        form = PostForm(request.POST or None, instance=post)
        if form.is_valid():
            form.save()
            return redirect('posts:post_detail', post_id)
        return render(request, 'posts/create_post.html', {'form': form})
    is_edit = True
    template = 'posts/create_post.html'
    context = {
        'form': form,
        'is_edit': is_edit,
    }
    return render(request, template, context)
