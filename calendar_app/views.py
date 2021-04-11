from django.shortcuts import render
from django.contrib.auth.decorators import login_required
import calendar
from calendar import HTMLCalendar
from datetime import datetime
# Create your views here.


@ login_required(login_url='/login')
def cal_date(request):
    # month = month.title()
    # month_number = list(calendar.month_name).index(month)
    # # to make sure that month_number is exactly integer
    # month_number = int(month_number)

    # Get current year
    now = datetime.now()
    current_year = now.year
    current_month = now.month

    # create a calendar
    cal = HTMLCalendar().formatmonth(current_year, current_month)

    return render(request, 'calendar_app/calendar.html', {
        'cal': cal,
    })
