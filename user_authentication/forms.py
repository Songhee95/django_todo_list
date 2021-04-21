from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User


class ShRegisterForm(UserCreationForm):
    username = forms.CharField(label='username', widget=forms.TextInput(
        attrs={'placeholder': 'Username'}))
    email = forms.CharField(label='email', widget=forms.TextInput(
        attrs={'placeholder': 'Email address'}))
    password1 = forms.CharField(label='password', widget=forms.TextInput(
        attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='confirm password', widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm password'}))

    class Meta:
        model = User
        fields = ['username', 'email', 'password1', 'password2']
