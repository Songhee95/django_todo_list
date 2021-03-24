from django.shortcuts import render, redirect


# Create your views here.


def registerPage(request):
    context = {}
    return render(request, 'user_authentication/register.html')


def loginPage(request):
    contest = {}
    return render(request, 'user_authentication/login.html')
