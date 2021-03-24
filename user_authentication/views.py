from django.shortcuts import render, redirect
from django.contrib.auth.forms import UserCreationForm

# Create your views here.


def registerPage(request):
    form = UserCreationForm()
    context = {"form": form}
    return render(request, 'user_authentication/register.html', context)


def loginPage(request):
    contest = {}
    return render(request, 'user_authentication/login.html')
