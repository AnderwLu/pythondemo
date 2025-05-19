from django.contrib import admin
from django.urls import path
from . import views

urlpatterns = [
    path("hello/", views.hello),
    path("", views.index),
    path("show_excel/", views.show_excel),
    path("userManage/", views.userManage),
    path("deepseek/", views.deepseek),
    path("deepseek_old/", views.deepseek_old),
    path("deepseek_ams/", views.deepseek_ams),
    path("deepseek_reasoning/", views.deepseek_reasoning),
]
