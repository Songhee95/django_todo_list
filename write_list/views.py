from django.shortcuts import render
import requests
from . import models

# Create your views here.


def index(request):
    new_list = request.POST.get('todo')
    print(new_list)
    exist_list = models.List.objects.all()

    if exist_list.count() == 0:
        models.List.objects.create(todo_list=new_list)

    try:
        models.List.objects.get(todo_list=new_list)
    except:
        print('no match')
        models.List.objects.create(todo_list=new_list)

    all_list = models.List.objects.all()
    send_data = {
        'add_list': all_list
    }
    return render(request, 'write_list/new_list.html', send_data)


def new_list(request):

    return render(request, 'write_list/new_list.html')
