from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
import requests
from . import models
# Create your views here.


def getData():
    all_list = models.List.objects.all()
    send_data = {
        'add_list': all_list
    }
    return send_data


def index(request):
    new_list = request.POST.get('todo')
    if new_list:
        exist_list = models.List.objects.all()

        if exist_list.count() == 0:
            models.List.objects.create(todo_list=new_list)

        try:
            models.List.objects.get(todo_list=new_list)
        except:
            print('no match')
            models.List.objects.create(todo_list=new_list)
    send_data = getData()
    return render(request, 'write_list/new_list.html', send_data)


def delete(request, list_id):
    selected = models.List.objects.get(pk=list_id)
    selected.delete()
    send_data = getData()
    return redirect('list:index')


def new_list(request):

    return render(request, 'write_list/new_list.html')
