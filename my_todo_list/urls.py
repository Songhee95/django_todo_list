"""my_todo_list URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf.urls import url
from django.contrib.auth import views as auth_views


urlpatterns = [
    path('', include('write_list.urls')),
    path('', include('user_authentication.urls')),
    path('', include('calendar_app.urls')),
    path('admin/', admin.site.urls),
    url('', include('pwa.urls')),
    path('pwd_reset_sent/', auth_views.PasswordResetDoneView.as_view(template_name='user_authentication/pwd_reset_sent.html'),
         name="password_reset_done"),

    path('reset/<uidb64>/<token>/',
         auth_views.PasswordResetConfirmView.as_view(template_name='user_authentication/pwd_reset_confirm.html'), name='password_reset_confirm'),

    path('pwd_reset_complete/', auth_views.PasswordResetCompleteView.as_view(template_name='user_authentication/pwd_reset_complete.html'),
         name="password_reset_complete"),
]
