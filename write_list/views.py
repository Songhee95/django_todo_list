import pytz
from tzlocal import get_localzone
import time
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
import requests
from . import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.utils.dateparse import parse_datetime
# Create your views here.
# Setting and aware local timezone
local_tz = get_localzone()
ts = time.time()
utc_now, now = datetime.utcfromtimestamp(ts), datetime.fromtimestamp(ts)
local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(local_tz)
assert local_now.replace(tzinfo=None)


def timezone_set(data_time):
    local_time = data_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_time


today = local_now
weekday = today.weekday()
start_delta = timezone.timedelta(days=weekday)
start_of_week = today - start_delta
week_dates_original = [start_of_week +
                       timezone.timedelta(days=i) for i in range(7)]
week_dates = []
week_days = []

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

start_date_for_filtering = week_dates_original[0].strftime('%Y-%m-%d 00:00:00')
last_date_for_filtering = week_dates_original[6].strftime('%Y-%m-%d 11:59:59')


def getData(userid, getAll):
    if getAll:
        user = models.List.objects.filter(
            user=userid).order_by('created').reverse()
    else:
        user = models.List.objects.filter(
            user=userid, created__gte=start_date_for_filtering, created__lte=last_date_for_filtering).order_by('created').reverse()
    list_array = []
    date_array = []
    for listEle in user:
        if listEle.created.strftime('%B, %d, %Y') not in date_array:
            date_array.append(listEle.created.strftime('%B, %d, %Y'))

        if listEle.cleared:
            status = 'checked'
        else:
            status = 'unchecked'

        add_list = {
            'cleared': status,
            "li": listEle.todo_list,
            "created": timezone_set(listEle.created).strftime('%B, %d, %Y'),
            "updated": timezone_set(listEle.updated_time).strftime('%B, %d, %Y, %I:%M'),
            "id": listEle.id,
        }
        list_array.append(add_list)

    send_data = {
        'add_list': list_array,
        'date_array': week_dates,
        'today': timezone_set(local_now),
        'local_now': local_now,
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

        month_date_sort = timezone_set(listEle.created).strftime('%B')
        if month_date_sort == today.strftime('%B'):
            add_list = {
                'cleared': status,
                "li": listEle.monthly_goal,
                "created": timezone_set(listEle.created).strftime('%B, %d, %Y'),
                "updated": timezone_set(listEle.updated_time).strftime('%B, %d, %Y'),
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
            models.List.objects.get(
                user_id=userid, created=today, todo_list=new_list)
        except:
            models.List.objects.create(
                user_id=userid, todo_list=new_list).save()
    # if request.POST.get('todo-by-date'):
    #     print(request.POST.get('todo-by-date'))
    #     user = models.List.objects.filter(user=userid, created__gte=start_date_for_filtering, created__lte=last_date_for_filtering).order_by('created').reverse()

    return render(request, 'write_list/new_list.html', getData(userid, False))


@ login_required(login_url='/login')
@ csrf_exempt
def modal_pop(request):

    return render(request, "write_list/modal_pop.html")


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
    if pageType == 'list':
        get_original_value = models.List.objects.get(pk=list_id)
        if request.POST.get('string'):
            print(request.POST.get('string'))
            get_original_value.todo_list = request.POST.get('string')
        elif request.POST.get('checked'):
            get_original_value.cleared = request.POST.get('checked')
        get_original_value.save()
    elif pageType == 'monthly':
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
