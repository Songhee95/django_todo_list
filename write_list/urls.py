from django.urls import path
from . import views

urlpatterns = [
    path('', views.index, name='index'),
    path('new_list', views.new_list, name='new_list'),
]
