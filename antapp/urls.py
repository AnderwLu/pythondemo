from django.contrib import admin
from django.urls import path
from . import views
from .views import deepseek_agent_stream
from .views_bank import bank_business, ams_agent

urlpatterns = [
    path("hello/", views.hello),
    path("", views.index),
    path("show_excel/", views.show_excel),
    path("userManage/", views.userManage),
    path("deepseek/", views.deepseek),
    path("deepseek_old/", views.deepseek_old),
    path("deepseek_ams/", views.deepseek_ams),
    path("deepseek_reasoning/", views.deepseek_reasoning),
    path("deepseek_agent_stream/", deepseek_agent_stream),
    
    # 银行业务代理系统路由 - 统一入口
    path('api/bank/business/', bank_business),
    path('api/bank/ams/', ams_agent),
]
