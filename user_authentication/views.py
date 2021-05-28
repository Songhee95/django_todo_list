from django.shortcuts import render, redirect
from django.contrib.auth import login, authenticate
from django.contrib.auth.forms import UserCreationForm
from django.contrib.auth.models import User

# Create your views here.
from .forms import ShRegisterForm
# flash messages after register
from django.contrib import messages

from django.contrib.auth import authenticate, login, logout


def registerPage(request):
    form = ShRegisterForm()

    if request.method == 'POST':
        form = ShRegisterForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, 'Account was created for ' + username)
            return redirect('/login')

    context = {"form": form}
    return render(request, 'user_authentication/register.html', context)


def loginPage(request):
    if request.method == 'POST':
        username = request.POST.get('username')
        password = request.POST.get('password')
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('/')
        else:
            messages.info(request, 'Username OR password is incorrect!')
    return render(request, 'user_authentication/login.html')


def forgotUsernamePage(request):
    response = ''
    if request.method == 'POST':
        response = 'no match'
        email = request.POST.get('email')
        firstName = request.POST.get('firstName').capitalize()
        user_info = User.objects.filter(
            email=email, first_name=firstName)
        if user_info:
            user = str(user_info[0])
            response = user

    return render(request, 'user_authentication/forgotUsername.html', {'response': response})
