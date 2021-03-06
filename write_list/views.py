import pytz
from tzlocal import get_localzone
import time
from datetime import datetime
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.models import User
from django.shortcuts import get_object_or_404, render, redirect
from django.http import HttpResponseRedirect, HttpResponse, Http404
import requests
from . import models
from django.views.decorators.csrf import csrf_exempt
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from django.utils.dateparse import parse_datetime

# email
from django.core.mail import EmailMessage, send_mail, EmailMultiAlternatives
from django.conf import settings
from django.contrib.sites.shortcuts import get_current_site
from django.urls import reverse
from django.template.loader import render_to_string

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
# week_days = []

for dates in week_dates_original:
    obj = {
        "date": dates.strftime('%B, %d, %Y'),
        'day': dates.strftime('%A'),
        'filtering_date': dates.strftime('%Y-%m-%d')
    }
    week_dates.append(obj)

    # week_dates.append(dates.strftime('%B, %d, %Y'))
    # week_days.append(dates.strftime('%A'))
# print(today.strftime('%B, %d, %Y, %I:%M'))
# print(date_7_days_ago)

start_date_for_filtering = week_dates[0]['filtering_date']+' 00:00:00'
last_date_for_filtering = week_dates[6]['filtering_date'] + ' 11:59:59'


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
            "created": listEle.created.strftime('%B, %d, %Y'),
            "updated": listEle.updated_time.strftime('%B, %d, %Y, %I:%M'),
            "id": listEle.id,
        }
        list_array.append(add_list)

    send_data = {
        'add_list': list_array,
        'date_array': week_dates,
        'today': timezone_set(local_now),
        'local_now': local_now.strftime('%B, %d, %Y'),
        'current_year': datetime.now().year,
        'current_month': datetime.now().month
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
        'add_list': list_array,
        'current_year': datetime.now().year,
        'current_month': datetime.now().month
    }
    return send_data


@ login_required(login_url='/login')
def index(request):
    userid = request.user.id
    if models.Joint.objects.filter(user=userid):
        joint_user_info = models.Joint.objects.filter(user=userid)
        for joint_user in joint_user_info:
            joint_user_data = getData(joint_user.joint_id, False)
            joint_user_name = User.objects.get(
                pk=joint_user.joint_id).first_name
    else:
        joint_user_data = ''
        joint_user_name = ''

    new_list = request.POST.get('todo')
    send_data = getData(userid, False)
    if new_list:
        if send_data == None:
            models.List.objects.create(
                user_id=userid, todo_list=new_list, created=now).save()
        try:
            models.List.objects.get(
                user_id=userid, created__year=today.year, created__month=today.month, created__day=today.day, todo_list=new_list)
        except:
            models.List.objects.create(
                user_id=userid, todo_list=new_list, created=now).save()
    send_data = {
        'user_data': getData(userid, False),
        'joint_data': joint_user_data,
        'joint_user_name': joint_user_name
    }

    return render(request, 'write_list/new_list.html', send_data)


@ login_required(login_url='/login')
@ csrf_exempt
def modal_pop(request):
    userid = request.user.id
    if request.POST.get('pageType'):
        modal_input = request.POST.get("string")
        modal_input_date = request.POST.get("date")
        modal_date_utc = datetime.strptime(
            modal_input_date, '%B, %d, %Y')
        print(modal_date_utc)
        print(modal_input_date)
        user = models.List.objects.filter(user=userid, created=modal_date_utc)
        if user == None:
            models.List.objects.create(
                user_id=userid, todo_list=modal_input, created=modal_date_utc).save()
        try:
            models.List.objects.get(
                user_id=userid, created=modal_date_utc, todo_list=modal_input)
        except:
            models.List.objects.create(
                user_id=userid, todo_list=modal_input, created=modal_date_utc).save()
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
        url = 'calendar/' + \
            str(datetime.now().year) + '/' + str(datetime.now().month)
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
        url = 'calendar_app/calendar.html'
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
        'user_data': {
            'current_year': datetime.now().year,
            'current_month': datetime.now().month
        },
        'daily': daily,
        'month': month,
        'current_year': datetime.now().year,
        'current_month': datetime.now().month
    }
    return render(request, 'write_list/history.html', send_data)


@ login_required(login_url='/login')
@ csrf_exempt
def invite(request):
    print(request.user)
    joint_status = models.Joint.objects.filter(user_id=request.user.id)
    if joint_status:
        for joint in joint_status:
            joint_name = User.objects.get(pk=joint.joint_id)
    else:
        joint_name = ''

    send_data = {
        'all_user': User.objects.all(),
        'joint_name': joint_name,
        'user_info': {
            'user_first_name': request.user.first_name,
            'user_last_name': request.user.last_name,
            'user_username': request.user.username,
            'user_email': request.user.email,
            'user_password': request.user.password,
        },
        'user_data': {
            'current_year': datetime.now().year,
            'current_month': datetime.now().month
        }
    }
    if request.POST.get('selected_user'):
        # Send invitation email
        selected_user = request.POST.get('selected_user')
        selected_user_pk = User.objects.get(username=selected_user).pk
        selected_user_firstname = User.objects.get(
            username=selected_user).first_name
        selected_user_email = User.objects.get(
            username=selected_user).email

        current_site = get_current_site(request)

        link = reverse('list:confirm', kwargs={
                       'selected_user': selected_user_pk,
                       'request_from': request.user.id})

        email_subject = 'SH Schedule App Invitation'
        confirm_url = 'http://'+current_site.domain+link

        template = render_to_string(
            'write_list/email_template.html', {'user_firstname': request.user.first_name, 'selected_user': selected_user_firstname, 'domain': confirm_url})

        # email = EmailMessage(
        #     email_subject,
        #     template,
        #     settings.EMAIL_HOST_USER,
        #     ['noros78342@laraskey.com'],
        # )

        email = EmailMultiAlternatives(
            email_subject, template, settings.EMAIL_HOST_USER,  [selected_user_email])
        email.attach_alternative(template, "text/html")
        email.fail_silently = False
        email.send()

    return render(request, 'write_list/invite.html', send_data)


def confirm(request, selected_user, request_from):
    get_selected_user = User.objects.get(pk=selected_user).first_name
    get_request_from_user = User.objects.get(pk=request_from).first_name
    print(selected_user)
    if request.POST.get("confirmed"):
        user_side_joint_status = models.Joint.objects.filter(
            user_id=request_from)
        if selected_user != request_from:
            print('good to go')
            try:
                models.Joint.objects.get(
                    user_id=request_from, joint_id=selected_user)
            except:
                models.Joint.objects.create(
                    user_id=request_from,  joint_id=selected_user).save()

            try:
                models.Joint.objects.get(
                    user_id=selected_user, joint_id=request_from)
            except:
                models.Joint.objects.create(
                    user_id=selected_user, joint_id=request_from).save()
            return render(request, 'write_list/after_confirmation.html')

    return render(request, 'write_list/confirmation_page.html', {'selected_user': selected_user, 'request_from': request_from, 'get_request_from_user': get_request_from_user, "get_selected_user": get_selected_user})


@ login_required(login_url='/login')
def logoutUser(request):
    logout(request)
    return redirect('/login')
