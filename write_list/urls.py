from django.urls import path
from . import views

app_name = 'list'
urlpatterns = [
    path('', views.index, name='index'),
    path('new_list', views.new_list, name='new_list'),
    path('modal_pop', views.modal_pop, name='modal_pop'),
    path('logout/', views.logoutUser, name='logout'),
    path('<int:list_id>', views.delete, name='delete'),
    path('edit/<int:list_id>', views.edit, name='edit'),
    path('history', views.history, name='history'),
    path('invite', views.invite, name='invite'),
    path('confirm/<int:selected_user>/<int:request_from>/',
         views.confirm, name='confirm'),
]
