from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
import requests
from . import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from datetime import date
# Create your views here.

today = date.today()


def getData(userid, getAll):
    if getAll:
        user = models.List.objects.filter(user=userid)
    else:
        user = models.List.objects.filter(
            user=userid, created__year=today.year, created__month=today.month, created__day=today.day)

    list_array = []
    for listEle in user:
        if listEle.cleared:
            status = 'checked'
        else:
            status = 'unchecked'

        add_list = {
            'cleared': status,
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


@login_required(login_url='/login')
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
    send_data = getData(userid, False)
    return render(request, 'write_list/new_list.html', send_data)


@login_required(login_url='/login')
def delete(request, list_id):
    userid = request.user.id
    selected = models.List.objects.get(pk=list_id)
    selected.delete()
    send_data = getData(userid, False)
    return redirect('list:index')


@login_required(login_url='/login')
@ csrf_exempt
def edit(request, list_id):
    userid = request.user.id
    edit_id = list_id
    get_original_value = models.List.objects.get(pk=list_id)
    if request.POST.get('string'):
        edit_string = request.POST.get('string')
        get_original_value.todo_list = edit_string
    elif request.POST.get('checked'):
        edit_cleared = request.POST.get('checked')
        get_original_value.cleared = edit_cleared

    get_original_value.save()
    send_data = getData(userid, False)
    return render(request, 'write_list/new_list.html', send_data)


@login_required(login_url='/login')
def new_list(request):

    return render(request, 'write_list/new_list.html')


@login_required(login_url='/login')
def history(request):
    userid = request.user.id
    send_data = getData(userid, True)
    return render(request, 'write_list/history.html', send_data)


@login_required(login_url='/login')
def month(request):
    userid = request.user.id
    return render(request, 'write_list/month.html')


@login_required(login_url='/login')
def logoutUser(request):
    logout(request)
    return redirect('/login')
