from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import calendar
from calendar import HTMLCalendar
from datetime import datetime
from write_list import models
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


def get_monthly_data(userid, getAll):
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
        'add_list': list_array,
    }
    return send_data


@ login_required(login_url='/login')
@ csrf_exempt
def cal_date(request, year, month):
    # Get current year
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    # create a calendar
    cal = HTMLCalendar().formatmonth(int(year), int(month))

    # change month idx to string
    month_name = change_month_name(month)

    # user monthly goal
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

    return render(request, 'calendar_app/calendar.html', {
        'cal': cal,
        'month': month_name,
        'current_year': current_year,
        'current_month': current_month,
        'data': get_monthly_data(userid, False),
    })
