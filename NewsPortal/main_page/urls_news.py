from django.urls import path
from .views import (
    NewsList, NewsDetail, NewsCreate,
    NewsDelete, NewsSearch, NewsUpdate
)
from django.views.decorators.cache import cache_page


urlpatterns = [
    path('', cache_page(300)(NewsList.as_view()), name='news_list'),
    path('search/', NewsSearch.as_view(), name='news_search'),
    path('create/', NewsCreate.as_view(), name='news_create'),
    path('<int:id>/', NewsDetail.as_view(), name='news_detail'),
    path('<int:id>/edit/', NewsUpdate.as_view(), name='news_edit'),
    path('<int:id>/delete/', NewsDelete.as_view(), name='news_delete'),
]
