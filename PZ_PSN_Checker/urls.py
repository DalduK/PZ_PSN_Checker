"""PZ_PSN_Checker URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.0/topics/http/urls/
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
from django.conf.urls import url
from django.contrib import admin
from django.contrib.auth.views import LoginView, LogoutView
from django.urls import path

from app import views
from templates import *

urlpatterns = [
    path('admin/', admin.site.urls),
    path('createitem/', views.add_item),
    path('createitemurl/', views.add_item_from_url),
    path('', views.item_list, name='items'),
    path('login/', LoginView.as_view(template_name='registration/login.html'), name="login"),
    path('logout/', LogoutView.as_view(template_name='logged-out.html')),
    path('register/', views.register, name='register'),
    path('items/', views.item_list, name='items'),
    path('user/', views.user_watched, name='useri'),
    url(r'^objects/(?P<oid>[0-9]+)/$', views.object_specific_view, name='objects'),
    url(r'^password/$', views.change_password, name='change_password'),
]
