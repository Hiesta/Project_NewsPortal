from django.urls import path
from .views import AllList

urlpatterns = [
    path('', AllList.as_view(), name='all_list')
]
