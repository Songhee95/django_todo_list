from django.urls import path
from . import views

app_name = 'calendar_app'
urlpatterns = [
    path('calendar', views.cal_date, name='cal_date')
]
