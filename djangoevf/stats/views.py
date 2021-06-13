from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from rest_framework import viewsets
import firebirdsql

from .models import Almacen
from .serializer import AlmacenSerializer


"""Datos para conexion"""
conn = firebirdsql.connect(
    host='sfan.ddns.net',
    database='C:\Microsip datos\PRUEBAS.FDB',
    port=2000,
    user='SYSDBA',
    password='flexracer',
    charset='WIN1251'
)
cur = conn.cursor()


def index(request):
    """ Atender la petición GET / """
    # Consulta para obtener todos los elementos de un modelo / tabla
    # Regresa un QuerySet es una lista de objetos de tipo Tour
    lista_almacen = Almacen.objects.all()

    return render(request, "stats/index.html", {"almacenes": lista_almacen})

def ventas(request, fecha):
    par = [fecha, fecha, 0, 'N', 0, 'a', 0, 'S']
    cur.execute("select * from VENTA_DESGL_PER(?, ?, ?, ?, ?, ?, ?, ?)", (par))
    ventas = cur.fetchall()
    datos = {
        "ventas":ventas,
        "fecha":fecha
    }           
    return render(request, "stats/ventas.html", datos)