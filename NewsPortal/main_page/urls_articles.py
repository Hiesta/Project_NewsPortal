from django.urls import path
from .views import (
    ArticleList, ArticleDetail, ArticleCreate,
    ArticleDelete, ArticleSearch, ArticleUpdate

)

urlpatterns = [
    path('', ArticleList.as_view(), name='article_list'),
    path('search/', ArticleSearch.as_view(), name='article_search'),
    path('create/', ArticleCreate.as_view(), name='article_create'),
    path('<int:id>/', ArticleDetail.as_view(), name='article_detail'),
    path('<int:id>/edit/', ArticleUpdate.as_view(), name='article_edit'),
    path('<int:id>/delete/', ArticleDelete.as_view(), name='article_delete'),
]
