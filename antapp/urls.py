from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.hello),
    path("", views.index),
    path("show_excel/", views.show_excel),
    path("userManage/", views.userManage),
    path("deepseek/", views.deepseek),
]
