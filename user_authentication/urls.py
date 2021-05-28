from django.urls import path
from . import views

app_name = 'user_authentication'
urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('forgotUsername/', views.forgotUsernamePage, name='forgotUsername'),
]
