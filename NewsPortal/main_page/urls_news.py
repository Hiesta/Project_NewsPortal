from django.urls import path
from .views import (
    NewsList, NewsDetail, NewsCreate,
    NewsDelete, NewsSearch, NewsUpdate

)

urlpatterns = [
    path('', NewsList.as_view(), name='news_list'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:id>/', NewsDetail.as_view(), name='news_detail'),
    path('<int:id>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('<int:id>/delete/', NewsDelete.as_view(), name='news_delete'),
]
