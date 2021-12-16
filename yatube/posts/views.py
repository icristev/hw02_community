from django.contrib.auth.decorators import login_required
from django.core.paginator import Paginator
from django.shortcuts import get_object_or_404, redirect, render

from .forms import PostForm
from .models import Group, Post


def index(request):
    template = 'posts/index.html'
    posts = Post.objects.all().order_by('-pub_date')
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': page_obj,
    }
    return render(request, template, context)


def group_posts(request, slug):
    template = 'posts/group_list.html'
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:10]
    paginator = Paginator(posts, 10)
    page_number = request.GET.get('page')
    page_obj = paginator.get_page(page_number)
    context = {
        'posts': page_obj,
        'group': group,
    }
    return render(request, template, context)


def profile(request):
    template = 'posts/profile.html'
    return render(request, template)


def post_detail(request):
    template = 'posts/post_detail.html'
    return render(request, template)


@login_required
def post_create(request):
    template = 'posts/create_post.html'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/profile/<username>/')
        return render(request, template, {'form': form})
    form = PostForm()
    is_edit = True
    context = {'form': form,
               'is_edit': is_edit}
    return render(request, template, context)


@login_required
def post_edit(request):
    template = 'posts/create_post.html'
    if request.method == 'POST':
        form = PostForm(request.POST)
        if form.is_valid():
            post = form.save(commit=False)
            post.author = request.user
            post.save()
            return redirect('/profile/<username>/')
        return render(request, template, {'form': form})
    form = PostForm()
    is_edit = False
    context = {'form': form,
               'is_edit': is_edit}
    return render(request, template, context)
