from django.contrib.auth import views as auth_views
from django.urls import path
from rest_framework import routers
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('venta/<fecha>/', views.ventas, name="ventas"),
]