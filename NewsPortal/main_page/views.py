from django.shortcuts import render
from django.views.generic import ListView, DetailView
from .models import Post


# Create your views here.
class PostList(ListView):
    model = Post
    ordering = 'time_post'
    template_name = 'news.html'
    context_object_name = 'news'

    def get_ordering(self):
        return ['-time_post']


class PostDetail(DetailView):
    model = Post
    pk_url_kwarg = 'id'
    template_name = 'post.html'
    context_object_name = 'post'
