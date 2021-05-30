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

    path('pwd_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name='user_authentication/pwd_reset_sent.html'),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='user_authentication/pwd_reset_confirm.html'), name='password_reset_confirm'),

    path('pwd_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user_authentication/pwd_reset_complete.html'),
         name="password_reset_complete"),

]
