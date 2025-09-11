# authorization/urls.py
from django.urls import path
from django.contrib.auth.views import LoginView, LogoutView
from .views import upgrade_me, BaseRegisterView

urlpatterns = [
    path('login/', LoginView.as_view(template_name='auth/login.html'), name='login'),
    path('logout/', LogoutView.as_view(template_name='auth/logout.html'), name='logout'),
    path('signup/', BaseRegisterView.as_view(template_name='auth/signup.html'), name='signup'),
    path('upgrade/', upgrade_me, name='upgrade'),
]
