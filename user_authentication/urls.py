from django.urls import path
from django.contrib.auth import views as auth_views
from . import views

app_name = 'user_authentication'
urlpatterns = [
    path('register/', views.registerPage, name='register'),
    path('login/', views.loginPage, name='login'),
    path('forgotUsername/', views.forgotUsernamePage, name='forgotUsername'),

    path('forgotPassword/', auth_views.PasswordResetView.as_view(template_name='user_authentication/forgotPassword.html'),
         name='password_reset'),


]
