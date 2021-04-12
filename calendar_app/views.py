from django.shortcuts import render
from django.contrib.auth.decorators import login_required
from django.views.decorators.csrf import csrf_exempt
import calendar
from calendar import HTMLCalendar
from datetime import datetime
# Create your views here.


def change_month_name(current_month):
    date_obj = datetime.strptime(str(current_month), "%m")
    month_name = date_obj.strftime('%B')
    return month_name


@ login_required(login_url='/login')
@ csrf_exempt
def cal_date(request, year, month):
    print(year)
    print(month)
    # Get current year
    # now = datetime.now()
    # current_year = now.year

    # create a calendar
    cal = HTMLCalendar().formatmonth(int(year), int(month))

    # change month idx to string
    month_name = change_month_name(month)
    return render(request, 'calendar_app/calendar.html', {
        'cal': cal,
        'month': month_name
    })


# @ login_required(login_url='/login')
# @ csrf_exempt
# def change_month(request):
#     now = datetime.now()
#     current_year = now.year
#     idx = request.POST.get('idx')
#     current_month = int(idx)

#     print(current_month)
#     cal = HTMLCalendar().formatmonth(current_year, current_month)
#     month_name = change_month_name(current_month)
#     print(month_name)
#     return render(request, 'calendar_app/calendar.html', {
#         'cal': cal,
#         'month': month_name
#     })
