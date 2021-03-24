from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
import requests
from . import models
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def getData():
    all_list = models.List.objects.all()
    list_array = []
    for listEle in all_list:
        add_list = {
            "li": listEle.todo_list,
            "created": listEle.created,
            "updated": listEle.updated_time,
            "id": listEle.id
        }
        list_array.append(add_list)
    send_data = {
        'add_list': list_array
    }
    return send_data


def index(request):
    new_list = request.POST.get('todo')
    if new_list:
        exist_list = models.List.objects.all()

        if exist_list.count() == 0:
            models.List.objects.create(todo_list=new_list).save()
        try:
            models.List.objects.get(todo_list=new_list)
        except:
            print('no match')
            models.List.objects.create(todo_list=new_list).save()
    send_data = getData()
    return render(request, 'write_list/new_list.html', send_data)


def delete(request, list_id):
    selected = models.List.objects.get(pk=list_id)
    selected.delete()
    send_data = getData()
    return redirect('list:index')


@ csrf_exempt
def edit(request, list_id):
    edit_string = request.POST.get('string')
    edit_id = list_id
    get_original_value = models.List.objects.get(pk=list_id)
    get_original_value.todo_list = edit_string
    get_original_value.save()
    send_data = getData()
    return render(request, 'write_list/new_list.html', send_data)


def new_list(request):

    return render(request, 'write_list/new_list.html')
