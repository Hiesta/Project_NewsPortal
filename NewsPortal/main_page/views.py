from django.contrib.auth.mixins import LoginRequiredMixin, PermissionRequiredMixin
from django.views.generic import (
    ListView, DetailView, CreateView, UpdateView, DeleteView
)
from django.shortcuts import render, get_object_or_404, redirect
from django.core.cache import cache
from django.core.mail import send_mail, mail_admins
from django.contrib import messages
from django.urls import reverse, reverse_lazy
from .filters import PostFilter
from .models import Post, UserSubs, Category
from .forms import PostForm
from .tasks import send_news_notification


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

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'Post-{self.kwargs["id"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'Post-{self.kwargs["id"]}', obj, 300)

        return obj


class NewsCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'news/news_create.html'
    success_url = reverse_lazy('news_list')
    permission_required = ('main_page.add_post',)

    def form_valid(self, form):
        form.instance.news_type = 'NEWS'
        response = super().form_valid(form)

        send_news_notification.delay(self.object.id)
        
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

    def get_object(self, *args, **kwargs):
        obj = cache.get(f'Post-{self.kwargs["id"]}', None)
        if not obj:
            obj = super().get_object(queryset=self.queryset)
            cache.set(f'Post-{self.kwargs["id"]}', obj, 300)

        return obj


class ArticleCreate(LoginRequiredMixin, PermissionRequiredMixin, CreateView):
    form_class = PostForm
    model = Post
    template_name = 'articles/article_create.html'
    success_url = reverse_lazy('article_list')
    permission_required = {'main_page.add_post', }

    def form_valid(self, form):
        form.instance.news_type = 'ARTICLES'
        response = super().form_valid(form)

        send_news_notification.delay(self.object.id)
        
        return response


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


def subscribe_to_category(request, category_id):
    if request.user.is_authenticated:
        category = get_object_or_404(Category, id=category_id)
        
        subscription, created = UserSubs.objects.get_or_create(
            user=request.user,
            category=category
        )
        
        if created:
            messages.success(request, f'Вы успешно подписались на категорию "{category.category_name}"')
        else:
            messages.info(request, f'Вы уже подписаны на категорию "{category.category_name}"')
    else:
        messages.error(request, 'Для подписки необходимо войти в систему')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


def unsubscribe_from_category(request, category_id):
    if request.user.is_authenticated:
        category = get_object_or_404(Category, id=category_id)
        
        try:
            subscription = UserSubs.objects.get(user=request.user, category=category)
            subscription.delete()
            messages.success(request, f'Вы отписались от категории "{category.category_name}"')
        except UserSubs.DoesNotExist:
            messages.info(request, f'Вы не подписаны на категорию "{category.category_name}"')
    else:
        messages.error(request, 'Для отписки необходимо войти в систему')
    
    return redirect(request.META.get('HTTP_REFERER', '/'))


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