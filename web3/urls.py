"""web3 URL Configuration

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/3.2/topics/http/urls/
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

import myApp
import api.urls
from myApp import views

urlpatterns = [
    path('', views.login),
    path('api/', include(api.urls)),
    path('login', views.login),
    url(r'^admin/', admin.site.urls),
    path('index/', myApp.views.index),
    path('logout/', myApp.views.logout),
    path('register', myApp.views.register),
    path('order-list1/', myApp.views.ids_index),
    path('order-details/', myApp.views.order_details),
    path('ids_admin/', myApp.views.ids_admin),
    path('welcome/', myApp.views.welcome),






]
