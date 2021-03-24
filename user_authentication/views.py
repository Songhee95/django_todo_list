from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from .models import *
# from .forms import CreateUserForm


def registerPage(request):
    form = UserCreationForm()

    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            print('-' * 20)
            print(form)
            form.save()
        else:
            print('not able')

    context = {"form": form}
    return render(request, 'user_authentication/register.html', context)


def loginPage(request):
    contest = {}
    return render(request, 'user_authentication/login.html')
