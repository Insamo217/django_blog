from django import forms
from .models import *
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User


class PostForm(forms.ModelForm):
    class Meta:
        model = Post
        fields = ['title', 'slug', 'text']

        widgets = {
            'title': forms.TextInput(attrs={'class': 'form-control'}),
            'slug': forms.TextInput(attrs={'class': 'form-control'}),
            'text': forms.Textarea(attrs={'class': 'form-control'})
        }

        def clean_slug(self):
            new_slug = self.cleaned_data['slug'].lower()

            if new_slug == 'create':
                raise ValidationError('Slug не может быть создан')
            return new_slug


class UserLoginForm(forms.Form):
    username = forms.CharField(label="", widget=forms.TextInput
                               (attrs={'placeholder': 'Введите имя здесь...'}))
    password = forms.CharField(label="", widget=forms.PasswordInput
                                (attrs={'placeholder': 'Введите пароль здесь...'}))


class UserRegistrationForm(forms.ModelForm):
    password = forms.CharField(widget=forms.PasswordInput
    (attrs={'placeholder': 'Введите пароль здесь...'}))
    confirm_password = forms.CharField(widget=forms.PasswordInput
    (attrs={'placeholder': 'Подтвердите пароль...'}))

    class Meta:
        model = User
        fields = {
            'username',
            'email',
        }

    def clean_confirm_password(self):
        password = self.cleaned_data.get('password')
        confirm_password = self.cleaned_data.get('confirm_password')
        if password != confirm_password:
            raise forms.ValidationError('Пароль не совпадает')
        return confirm_password

