from django import forms
from django.contrib.auth.models import User


class UserProfileForm(forms.ModelForm):
    """Форма для редактирования профиля пользователя"""
    
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'email']
        widgets = {
            'username': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя пользователя'
            }),
            'first_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Имя'
            }),
            'last_name': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Фамилия'
            }),
            'email': forms.EmailInput(attrs={
                'class': 'form-control',
                'placeholder': 'Email'
            }),
        }
        labels = {
            'username': 'Имя пользователя',
            'first_name': 'Имя',
            'last_name': 'Фамилия',
            'email': 'Email',
        }
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Делаем поля обязательными
        self.fields['first_name'].required = True
        self.fields['last_name'].required = True
        self.fields['email'].required = True