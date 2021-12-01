from django.shortcuts import get_object_or_404, render
from .models import Post, Group


def index(request):
    posts = Post.objects.all()[:10]
    template = 'posts/index.html'
    title = 'Последние обновления на сайте'
    context = {
        'title': title,
        'posts': posts,
    }
    return render(request, template, context)


def group_list(request):
    template = 'posts/group_list.html'
    title = 'Список групп'
    text = 'Информация о группах проекта Yatube'
    context = {
        'text': text,
        'title': title,
    }
    return render(request, template, context)


def group_posts(request, slug):
    group = get_object_or_404(Group, slug=slug)
    posts = group.posts.all()[:10]
    trmplate = 'posts/group_list.html'
    context = {
        'group': group,
        'posts': posts,
    }
    return render(request, trmplate, context)
