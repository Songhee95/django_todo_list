from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm

# Create your views here.
from .forms import ShRegisterForm


def registerPage(request):
    form = ShRegisterForm()

    if request.method == 'POST':
        form = ShRegisterForm(request.POST)
        if form.is_valid():
            form.save()

    context = {"form": form}
    return render(request, 'user_authentication/register.html', context)


def loginPage(request):
    contest = {}
    return render(request, 'user_authentication/login.html')
