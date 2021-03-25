from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
import requests
from . import models
from django.views.decorators.csrf import csrf_exempt
# Create your views here.


def getData(userid):
    user = models.List.objects.filter(user=userid)
    list_array = []
    for listEle in user:
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


# @login_required(login_url='login')
def index(request):
    userid = request.user.id
    new_list = request.POST.get('todo')
    if new_list:
        exist_list = getData(userid)
        if exist_list == None:
            models.List.objects.create(
                user_id=userid, todo_list=new_list).save()
        try:
            models.List.objects.get(user_id=userid, todo_list=new_list)
        except:
            print('no match')
            models.List.objects.create(
                user_id=userid, todo_list=new_list).save()
    send_data = getData(userid)
    return render(request, 'write_list/new_list.html', send_data)


def delete(request, list_id):
    userid = request.user.id
    selected = models.List.objects.get(pk=list_id)
    selected.delete()
    send_data = getData(userid)
    return redirect('list:index')


@ csrf_exempt
def edit(request, list_id):
    userid = request.user.id
    edit_string = request.POST.get('string')
    edit_id = list_id
    get_original_value = models.List.objects.get(pk=list_id)
    get_original_value.todo_list = edit_string
    get_original_value.save()
    send_data = getData(userid)
    return render(request, 'write_list/new_list.html', send_data)


def new_list(request):

    return render(request, 'write_list/new_list.html')


def logoutUser(request):
    logout(request)
    return redirect('/login')
