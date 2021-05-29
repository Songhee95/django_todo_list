from django import forms
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User
from django.core.exceptions import ValidationError


class ShRegisterForm(UserCreationForm):
    first_name = forms.CharField(label='First Name : ', widget=forms.TextInput(
        attrs={'placeholder': 'First Name'}))
    last_name = forms.CharField(label='Last Name: ', widget=forms.TextInput(
        attrs={'placeholder': "Last Name"}))
    username = forms.CharField(label='User Name: ', widget=forms.TextInput(
        attrs={'placeholder': 'Username'}))
    email = forms.CharField(label='Email: ', widget=forms.TextInput(
        attrs={'placeholder': 'Email address'}))
    password1 = forms.CharField(label='Password: ', widget=forms.PasswordInput(
        attrs={'placeholder': 'Password'}))
    password2 = forms.CharField(label='Confirm Password: ', widget=forms.PasswordInput(
        attrs={'placeholder': 'Confirm password'}))

    def clean_email(self):
        email = self.cleaned_data['email'].lower()
        r = User.objects.filter(email=email)
        if r.count():
            raise ValidationError('Email already exists')
        return email

    class Meta:
        model = User
        fields = ['first_name', 'last_name', 'username',
                  'email', 'password1', 'password2']
