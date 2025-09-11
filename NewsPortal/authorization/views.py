from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.models import User, Group
from django.views.generic.edit import CreateView, UpdateView
from django.contrib.auth.decorators import login_required
from django.contrib.auth.mixins import LoginRequiredMixin
from django.urls import reverse_lazy
from django.contrib import messages
from .models import BaseRegisterForm
from .forms import UserProfileForm


class BaseRegisterView(CreateView):
    model = User
    form_class = BaseRegisterForm
    success_url = '/'


@login_required
def upgrade_me(request):
    user = request.user
    author_group = Group.objects.get(name='authors')
    if not request.user.groups.filter(name='authors').exists():
        author_group.user_set.add(user)
    return redirect('/')


@login_required
def profile_view(request):
    """Личный кабинет пользователя"""
    user = request.user
    user_groups = user.groups.all()
    return render(request, 'auth/profile.html', {
        'user': user,
        'user_groups': user_groups,
    })


class ProfileEditView(LoginRequiredMixin, UpdateView):
    """Редактирование профиля пользователя"""
    model = User
    form_class = UserProfileForm
    template_name = 'auth/profile_edit.html'
    success_url = reverse_lazy('profile')
    
    def get_object(self):
        return self.request.user
    
    def form_valid(self, form):
        messages.success(self.request, 'Профиль успешно обновлен!')
        return super().form_valid(form)


