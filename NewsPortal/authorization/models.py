from django.db import models
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User, Group
from allauth.account.forms import SignupForm
from django import forms


class BaseRegisterForm(UserCreationForm):
    email = forms.EmailField(label='Email')
    first_name = forms.CharField(label='First Name')
    last_name = forms.CharField(label='Last Name')

    class Meta:
        model = User
        fields = ("username",
                  'first_name',
                  'last_name',
                  'email',
                  'password1',
                  'password2')

    # def save(self, commit=True):
    #     user = super().save(commit)
    #     common_group = Group.objects.get(name='common')
    #     user.groups.add(common_group)
    #     return user


class BasicSignupForm(SignupForm):

    def save(self, request):
        user = super(BasicSignupForm, self).save(request)
        common_group = Group.objects.get(name='common')
        common_group.user_set.add(user)
        return user
