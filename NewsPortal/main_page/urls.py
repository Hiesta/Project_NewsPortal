from django.urls import path
from .views import AllList, subscribe_to_category, unsubscribe_from_category

urlpatterns = [
    path('', AllList.as_view(), name='all_list'),
    path('subscribe/<int:category_id>/', subscribe_to_category, name='subscribe_category'),
    path('unsubscribe/<int:category_id>/', unsubscribe_from_category, name='unsubscribe_category'),
]
