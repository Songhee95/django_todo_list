from django.urls import path
from . import views

app_name = 'calendar_app'
urlpatterns = [
    path('calendar/<int:year>/<str:month>', views.cal_date, name='cal_date'),
    path('add_schedule', views.add_schedule, name='add_schedule'),
]
