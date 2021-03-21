from django.shortcuts import render
import requests


# Create your views here.
def index(request):
    return render(request, 'index.html')


def new_list(request):
    new_list = request.POST.get('todo')
    print(new_list)
    send_data = {
        'add_list': new_list
    }
    return render(request, 'write_list/new_list.html', send_data)
