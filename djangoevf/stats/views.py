from datetime import datetime, timezone
from django.contrib.auth import authenticate, login, logout
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User
from django.shortcuts import render, redirect
from rest_framework import viewsets
import firebirdsql

from .models import Almacen
from .serializer import AlmacenSerializer


"""Datos para conexion a base de datos remota"""
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
    """ Atender la petición GET Y POST / """
    mensaje = ""
    if request.method == "POST":
        username = request.POST.get("username")
        password = request.POST.get("password")
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect(request.GET.get("next", "dash"))
        else:
            mensaje = "USUARIO O PASSWORD ES INCORRECTO"
  
    return render(request, "stats/index.html", {"mensaje" : mensaje})

@login_required
def ventasAPI(request, fecha):
    par = [fecha, fecha, 0, 'N', 0, 'a', 0, 'S']
    cur.execute("select * from VENTA_DESGL_PER(?, ?, ?, ?, ?, ?, ?, ?)", (par))
    ventas = cur.fetchall()
    datos = {
        "ventas":ventas,
        "fecha":fecha
    }           
    return render(request, "stats/ventas.html", datos)

@login_required
def ventas(request):
    fecha = request.GET.get("fecha")
    """JUGANDO CON EL FORMATO DE LA FECHA LUEGO LO CAMBIO"""
    print(type(fecha))
    print(fecha)
    date=datetime.strptime(fecha, '%Y-%m-%d')
    print(date)
    print(date.strftime('%d.%m.%Y'))
    fechabuena = date.strftime('%d.%m.%Y')
    par = [fechabuena, fechabuena, 0, 'N', 0, 'a', 0, 'S']
    cur.execute("select * from VENTA_DESGL_PER(?, ?, ?, ?, ?, ?, ?, ?)", (par))
    ventas = cur.fetchall()
    datos = {
        "ventas":ventas,
        "fecha":fechabuena
    }           
    return render(request, "stats/ventas.html", datos)


@login_required
def dash(request):
    now = datetime.now()
    return render(request, "stats/dash.html", {"now" : now})

def salir(request):
    logout(request)
    return redirect("/")

@login_required
def articulo(request):
    modelo = request.GET.get("modelo")
    par = [modelo, 19]
    cur.execute("select TALLA, EXISTENCIA from VT_BUSCA_MODELO_TALLAS(?, ?) order by TALLA asc", (par))
    almacentj = cur.fetchall()
    datos = {
        "almacentj":almacentj,
        "modelo":modelo
    }
    print(almacentj)
    return render(request, "stats/articulo.html", datos)
