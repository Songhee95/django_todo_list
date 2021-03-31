import pytz
import datetime
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
import requests
from . import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
import calendar
# Create your views here.

today = timezone.now()
weekday = today.weekday()
start_delta = timezone.timedelta(days=weekday)
start_of_week = today - start_delta
week_dates_original = [start_of_week +
                       timezone.timedelta(days=i) for i in range(7)]
week_dates = []
week_days = []
date_7_days_ago = today - timezone.timedelta(days=7)

print(today)

for dates in week_dates_original:
    obj = {
        "date": dates.strftime('%B, %d, %Y'),
        'day': dates.strftime('%A')
    }
    week_dates.append(obj)
    # week_dates.append(dates.strftime('%B, %d, %Y'))
    # week_days.append(dates.strftime('%A'))
# print(today.strftime('%B, %d, %Y, %I:%M'))
# print(date_7_days_ago)


def getData(userid, getAll):

    if getAll:
        user = models.List.objects.filter(
            user=userid).order_by('created').reverse()
    else:
        user = models.List.objects.filter(
            user=userid, created__gte=date_7_days_ago).order_by('created').reverse()
    list_array = []
    date_array = []
    # print(user)
    for listEle in user:
        print(
            listEle.updated_time.strftime('%B, %d, %Y, %I:%M'))
        if listEle.created.strftime('%B, %d, %Y') not in date_array:
            date_array.append(listEle.created.strftime('%B, %d, %Y'))

        if listEle.cleared:
            status = 'checked'
        else:
            status = 'unchecked'

        add_list = {
            'cleared': status,
            "li": listEle.todo_list,
            "created": listEle.created.strftime('%B, %d, %Y'),
            "updated": listEle.updated_time.strftime('%B, %d, %Y, %I:%M'),
            "id": listEle.id,
        }
        list_array.append(add_list)

    send_data = {
        'add_list': list_array,
        'date_array': week_dates
    }
    return send_data


def get_monthly_data(userid, getAll):
    if getAll:
        user = models.Monthly.objects.filter(
            user=userid).order_by('created').reverse()
    else:
        user = models.Monthly.objects.filter(
            user=userid, created__year=today.year, created__month=today.month).order_by('created').reverse()

    list_array = []
    for listEle in user:
        if listEle.cleared:
            status = 'checked'
        else:
            status = 'unchecked'

        add_list = {
            'cleared': status,
            "li": listEle.monthly_goal,
            "created": listEle.created.strftime('%B, %d, %Y'),
            "updated": listEle.updated_time.strftime('%B, %d, %Y'),
            "id": listEle.id
        }
        list_array.append(add_list)

    send_data = {
        'add_list': list_array
    }
    return send_data


@ login_required(login_url='/login')
def index(request):
    userid = request.user.id
    new_list = request.POST.get('todo')
    send_data = getData(userid, False)
    if new_list:
        if send_data == None:
            models.List.objects.create(
                user_id=userid, todo_list=new_list).save()
        try:
            models.List.objects.get(user_id=userid, todo_list=new_list)
        except:
            print('no match')
            models.List.objects.create(
                user_id=userid, todo_list=new_list).save()

    return render(request, 'write_list/new_list.html', getData(userid, False))


@ login_required(login_url='/login')
def delete(request, list_id):
    userid = request.user.id
    url = 'list:index'
    if request.POST.get('list_delete'):
        selected = models.List.objects.get(pk=list_id)
        selected.delete()
        send_data = getData(userid, False)
    elif request.POST.get('month_delete'):
        selected = models.Monthly.objects.get(pk=list_id)
        selected.delete()
        send_data = get_monthly_data(userid, False)
        url = 'list:month'
    return redirect(url)


@ login_required(login_url='/login')
@ csrf_exempt
def edit(request, list_id):
    userid = request.user.id
    edit_id = list_id
    pageType = request.POST.get('pageType')
    send_data = getData(userid, False)
    url = 'write_list/new_list.html'

    if pageType == 'list_clear':
        get_original_value = models.List.objects.get(pk=list_id)
        if request.POST.get('string'):
            get_original_value.todo_list = request.POST.get('string')
        elif request.POST.get('checked'):
            get_original_value.cleared = request.POST.get('checked')
        get_original_value.save()
    elif pageType == 'monthly_clear':
        get_original_value = models.Monthly.objects.get(pk=list_id)
        if request.POST.get('string'):
            get_original_value.monthly_goal = request.POST.get('string')
        elif request.POST.get('checked'):
            get_original_value.cleared = request.POST.get('checked')
        get_original_value.save()
        send_data = get_monthly_data(userid, False)
        url = 'write_list/month.html'
    return render(request, url, send_data)


@ login_required(login_url='/login')
def new_list(request):

    return render(request, 'write_list/new_list.html')


@ login_required(login_url='/login')
def history(request):
    userid = request.user.id
    daily = getData(userid, True)
    month = get_monthly_data(userid, True)
    send_data = {
        'daily': daily,
        'month': month,
    }
    return render(request, 'write_list/history.html', send_data)


@ login_required(login_url='/login')
def month(request):
    userid = request.user.id
    new_list = request.POST.get('monthly')
    send_data = get_monthly_data(userid, False)
    if new_list:
        if send_data == None:
            models.Monthly.objects.create(
                user_id=userid, monthly_goal=new_list).save()
        try:
            models.Monthly.objects.get(
                user_id=userid, monthly_goal=new_list)
        except:
            print('no match')
            models.Monthly.objects.create(
                user_id=userid, monthly_goal=new_list).save()
    send_data = {
        'data': get_monthly_data(userid, False),
        'date': today.strftime('%B')
    }
    return render(request, 'write_list/month.html', send_data)


@ login_required(login_url='/login')
def logoutUser(request):
    logout(request)
    return redirect('/login')
