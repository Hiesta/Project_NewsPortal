from django import forms
from django.core.exceptions import ValidationError
from .models import Post


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = [
            'news_type',
            'author',
            'category',
            'header',
            'body',
        ]

    def clean(self):
        cleaned_data = super().clean()
        header = cleaned_data.get('header')
        body = cleaned_data.get('body')
        if not header:
            raise ValidationError({
                'header': 'Header cannot be empty'
            })
        if not body:
            raise ValidationError({
                'body': 'Body cannot be empty'
            })
        return cleaned_data
