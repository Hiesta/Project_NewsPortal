from django_filters import FilterSet, DateFilter
from django import forms
from .models import Post


class PostFilter(FilterSet):
    date_after = DateFilter(
        field_name="time_post",
        lookup_expr='gt',
        label="Позже даты",
        widget=forms.DateInput(attrs={'type': 'date'})
    )

    class Meta:
        model = Post
        fields = {
            'header': ['icontains'],
            'author': ['exact'],
        }
