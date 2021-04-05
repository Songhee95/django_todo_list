from django.urls import path
from . import views

app_name = 'list'
urlpatterns = [
    path('', views.index, name='index'),
    path('new_list', views.new_list, name='new_list'),
    path('modal', views.modal, name='modal'),
    path('logout/', views.logoutUser, name='logout'),
    path('<int:list_id>', views.delete, name='delete'),
    path('edit/<int:list_id>', views.edit, name='edit'),
    path('history', views.history, name='history'),
    path('month', views.month, name='month'),
]
