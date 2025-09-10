from django.shortcuts import render
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .filters import PostFilter
from .models import Post
from .forms import PostForm


# XXX: ====================== NEWS ======================
class NewsList(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(news_type='NEWS').order_by('-time_post')


class NewsDetail(DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Post.objects.filter(news_type='NEWS')


class NewsCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/news_create.html'
    success_url = reverse_lazy('news_list')

    def form_valid(self, form):
        form.instance.news_type = 'NEWS'
        return super().form_valid(form)


class NewsUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('news_list')

    def get_queryset(self):
        return Post.objects.filter(news_type='NEWS')


class NewsDelete(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('news_list')
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Post.objects.filter(news_type='NEWS')


class NewsSearch(NewsList):
    template_name = 'news/news_search.html'

    def get_queryset(self):
        queryset = Post.objects.filter(news_type='news').order_by('-time_post')
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# XXX: ====================== ARTICLES ======================
class ArticleList(ListView):
    model = Post
    template_name = 'articles/article_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(news_type='POST').order_by('-time_post')


class ArticleDetail(DetailView):
    model = Post
    template_name = 'articles/article_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Post.objects.filter(news_type='POST')


class ArticleCreate(CreateView):
    form_class = PostForm
    model = Post
    template_name = 'articles/article_create.html'
    success_url = reverse_lazy('article_list')

    def form_valid(self, form):
        form.instance.news_type = 'POST'
        return super().form_valid(form)


class ArticleUpdate(UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'articles/article_edit.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('article_list')

    def get_queryset(self):
        return Post.objects.filter(news_type='POST')


class ArticleDelete(DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('article_list')
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Post.objects.filter(news_type='POST')


class ArticleSearch(ArticleList):
    template_name = 'articles/article_search.html'

    def get_queryset(self):
        queryset = Post.objects.filter(news_type='POST').order_by('-time_post')
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# XXX: --- OLD VERSION ---
# class PostList(ListView):
#     model = Post
#     ordering = 'time_post'
#     template_name = 'news.html'
#     context_object_name = 'news'
#     paginate_by = 10
#
#     def get_ordering(self):
#         return ['-time_post']
#
#
# class PostListWithFilter(PostList):
#     template_name = 'search.html'
#
#     def get_queryset(self):
#         queryset = super().get_queryset()
#         self.filterset = PostFilter(self.request.GET, queryset)
#         return self.filterset.qs
#
#     def get_context_data(self, **kwargs):
#         context = super().get_context_data(**kwargs)
#         context['filterset'] = self.filterset
#         return context
#
#
# class PostDetail(DetailView):
#     model = Post
#     pk_url_kwarg = 'id'
#     template_name = 'post.html'
#     context_object_name = 'post'
#
#
# class PostCreate(CreateView):
#     form_class = PostForm
#     model = Post
#     template_name = 'post_edit.html'
#
#
# class PostUpdate(UpdateView):
#     form_class = PostForm
#     model = Post
#     template_name = 'post_edit.html'
#     pk_url_kwarg = 'id'
#     success_url = reverse_lazy('all_news')
#
#
# class PostDelete(DeleteView):
#     model = Post
#     template_name = 'post_delete.html'
#     success_url = reverse_lazy('all_news')
#     pk_url_kwarg = 'id'
