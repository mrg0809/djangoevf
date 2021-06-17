from django.contrib.auth import views as auth_views
from django.urls import path
from rest_framework import routers
from . import views

urlpatterns = [
    path('', views.index, name="index"),
    path('venta/<fecha>/', views.ventasAPI, name="ventasAPI"),
    path('venta/', views.ventas, name="ventas"),
    path('articulo/<modelo>/', views.articulo, name="articulo"),
    path('articulo/', views.articulo, name="articulo"),
    path('accounts/login/', views.index, name="index"),
    path('dash/', views.dash, name="dash"),
    path('accounts/logout/', views.salir, name="logout"),
]