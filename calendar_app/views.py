from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from write_list import models
from . import models as calModels
import pytz
from tzlocal import get_localzone
import time
# Create your views here.

local_tz = get_localzone()
ts = time.time()
utc_now, now = datetime.utcfromtimestamp(ts), datetime.fromtimestamp(ts)
local_now = utc_now.replace(tzinfo=pytz.utc).astimezone(local_tz)
assert local_now.replace(tzinfo=None)


def timezone_set(data_time):
    local_time = data_time.replace(tzinfo=pytz.utc).astimezone(local_tz)
    return local_time


today = local_now


def change_month_name(current_month):
    date_obj = datetime.strptime(str(current_month), "%m")
    month_name = date_obj.strftime('%B')
    return month_name


def get_monthly_data(userid, getAll, year, month):
    user = models.Monthly.objects.filter(
        user=userid, created__year=year, created__month=month).order_by('created').reverse()
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
                "id": listEle.id
            }
            list_array.append(add_list)
    send_data = {
        'add_list': list_array,
    }
    return send_data


# Get current year
now = datetime.now()
current_year = now.year
current_month = now.month


@ login_required(login_url='/login')
@ csrf_exempt
def cal_date(request, year, month):
    userid = request.user.id
    # create a calendar
    cal = HTMLCalendar().formatmonth(int(year), int(month))

    # change month idx to string
    month_name = change_month_name(month)

    # user monthly goal
    userid = request.user.id
    new_list = request.POST.get('monthly')
    send_data = get_monthly_data(userid, False, year, month)
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

    schedule_data = calModels.Month_Schedule.objects.filter(
        user_id=userid, created__year=year, created__month=month)

    return render(request, 'calendar_app/calendar.html', {
        'cal': cal,
        'month': month_name,
        'current_year': current_year,
        'current_month': current_month,
        'data': get_monthly_data(userid, False, year, month),
        'schedule': schedule_data
    })


@ login_required(login_url='/login')
@ csrf_exempt
def add_schedule(request):
    userid = request.user.id
    # create a calendar
    cal = HTMLCalendar().formatmonth(int(current_year), int(current_month))
    # new_to_calendar = request.POST.get('schedule')
    add_to_cal_month = int(request.POST.get('month'))
    add_to_cal_day = int(request.POST.get('day'))
    add_to_cal_value = request.POST.get('value')

    add_to_cal_created = datetime(
        current_year, add_to_cal_month, add_to_cal_day)

    print(add_to_cal_value)
    if add_to_cal_value:
        user = calModels.Month_Schedule.objects.create(
            user_id=userid, schedule=add_to_cal_value, created=add_to_cal_created)

    url = 'calendar/' + \
        str(current_year) + '/' + str(current_month)
    return redirect(url)


@ login_required(login_url='/login')
@ csrf_exempt
def delete(request):
    userid = request.user.id
    schedule_id = request.POST.get('id')
    selected = calModels.Month_Schedule.objects.get(pk=schedule_id)
    selected.delete()
    return redirect('/')
