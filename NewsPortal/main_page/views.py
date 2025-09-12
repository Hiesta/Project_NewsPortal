from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.shortcuts import render
from django.core.mail import send_mail, mail_admins
from django.urls import reverse, reverse_lazy
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from .filters import PostFilter
from .models import Post, UserSubs
from .forms import PostForm


class AllList(LoginRequiredMixin, ListView):
    model = Post
    ordering = 'time_post'
    template_name = 'all_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_ordering(self):
        return ['-time_post']

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['is_not_author'] = not self.request.user.groups.filter(name='authors').exists()
        return context


# XXX: ====================== NEWS ======================
class NewsList(ListView):
    model = Post
    template_name = 'news/news_list.html'
    context_object_name = 'posts'
    paginate_by = 10

    def get_queryset(self):
        return Post.objects.filter(news_type='NEWS').order_by('-time_post')


class NewsDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'news/news_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Post.objects.filter(news_type='NEWS')


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/news_create.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('main_page.add_post',)

    def form_valid(self, form):
        form.instance.news_type = 'NEWS'
        response = super().form_valid(form)

        post = self.object
        categories = post.category.all()

        subscribers_emails = []
        for category in categories:
            subscribers = category.subscribers.all()
            subscribers_emails += [user.email for user in subscribers]

        subscribers_emails = list(set(subscribers_emails))
        if subscribers_emails:
            send_mail(
                subject=f'Новая новость в категории: {", ".join(
                    [c.category_name for c in categories]
                )}',
                message=f'{post.header}\n\n{post.body[:50]}',
                from_email='anton@yandex.ru',
                recipient_list=subscribers_emails
            )
        return response


class NewsUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'news/news_edit.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('news_list')
    permission_required = {'main_page.change_post', }

    def get_queryset(self):
        return Post.objects.filter(news_type='NEWS')


class NewsDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('news_list')
    pk_url_kwarg = 'id'
    permission_required = {'main_page.delete_post', }

    def get_queryset(self):
        return Post.objects.filter(news_type='NEWS')


class NewsSearch(NewsList):
    template_name = 'news/news_search.html'

    def get_queryset(self):
        queryset = Post.objects.filter(news_type='NEWS').order_by('-time_post')
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
        return Post.objects.filter(news_type='ARTICLES').order_by('-time_post')


class ArticleDetail(LoginRequiredMixin, DetailView):
    model = Post
    template_name = 'articles/article_detail.html'
    context_object_name = 'post'
    pk_url_kwarg = 'id'

    def get_queryset(self):
        return Post.objects.filter(news_type='ARTICLES')


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'articles/article_create.html'
    success_url = reverse_lazy('article_list')
    permission_required = {'main_page.add_post', }

    def form_valid(self, form):
        form.instance.news_type = 'ARTICLES'
        return super().form_valid(form)


class ArticleUpdate(LoginRequiredMixin, PermissionRequiredMixin, UpdateView):
    form_class = PostForm
    model = Post
    template_name = 'articles/article_edit.html'
    pk_url_kwarg = 'id'
    success_url = reverse_lazy('article_list')
    permission_required = {'main_page.change_post',}

    def get_queryset(self):
        return Post.objects.filter(news_type='ARTICLES')


class ArticleDelete(LoginRequiredMixin, PermissionRequiredMixin, DeleteView):
    model = Post
    template_name = 'post_confirm_delete.html'
    success_url = reverse_lazy('article_list')
    pk_url_kwarg = 'id'
    permission_required = ('main_page.delete_post',)

    def get_queryset(self):
        return Post.objects.filter(news_type='ARTICLES')


class ArticleSearch(ArticleList):
    template_name = 'articles/article_search.html'

    def get_queryset(self):
        queryset = Post.objects.filter(news_type='ARTICLES').order_by('-time_post')
        self.filterset = PostFilter(self.request.GET, queryset=queryset)
        return self.filterset.qs

    def get_context_data(self, **kwargs):
        context = super().get_context_data(**kwargs)
        context['filterset'] = self.filterset
        return context


# XXX: --- OLD VERSION ---
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
