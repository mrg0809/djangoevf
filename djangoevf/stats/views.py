from datetime import datetime, timedelta, timezone
from os import replace
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
    database='C:\Microsip datos\SPORTS FAN 2016.FDB',
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
    print(ventas)
    total = 0
    for x in ventas:
        total = total+x[4]
        
    datos = {
        "ventas":ventas,
        "fecha":fechabuena,
        "total":total
    }           
    return render(request, "stats/ventas.html", datos)


@login_required
def dash(request):
    """VARIABLES DE FECHAS"""
    now = datetime.now()
    fecha = datetime.today().strftime('%d.%m.%Y')
    ayer = (datetime.today() - timedelta(days=1)).strftime('%d.%m.%Y')
    primerdia = datetime.today().replace(day=1).strftime('%d.%m.%Y')
    primerdiaaa = (datetime.today() - timedelta(days=365)).replace(day=1).strftime('%d.%m.%Y')
    primerdiaproxmes = (datetime.today().replace(day=28) + timedelta(days=4))
    ultimodiaaa = (primerdiaproxmes - timedelta(days=primerdiaproxmes.day)).replace(year=2020)

    
    """OBTENER VENTA AL MOMENTO"""
    par = [fecha, fecha, 0, 'N']
    cur.execute("select * from VENTA_TOTAL_PER_PV(?, ?, ?, ?)", (par))
    venta = cur.fetchone()

    """OBTENER VENTA POR TIENDAS DE AYER"""
    parayer = [ayer, ayer, 0, 'N', 0, 'a', 0, 'S']
    cur.execute("select * from VENTA_DESGL_PER(?, ?, ?, ?, ?, ?, ?, ?)",(parayer))
    ventas = cur.fetchall()
    total = 0
    for x in ventas:
        total = total+x[4]

    """OBTENER TRANSACCIONES POR TIENDAS DE HOY"""
    partrans = [fecha, fecha, 0, 'N', 0, 'a', 0, 'S']
    cur.execute("select * from VENTA_DESGL_PER(?, ?, ?, ?, ?, ?, ?, ?)",(partrans))
    transacciones = cur.fetchall()
    totaltransacciones = 0
    for y in transacciones:
        totaltransacciones = totaltransacciones+y[3]
    totaltransacciones = int(totaltransacciones)

    """TICKET PROMEDIO"""
    ticket = format(venta[0]/totaltransacciones, '.2f')

    """VENTA EN MES"""
    parmesactual = [primerdia, fecha, 0, 'N']
    cur.execute("select * from VENTA_TOTAL_PER_PV(?, ?, ?, ?)", (parmesactual))
    ventames = cur.fetchone()

    """VENTA MES AA"""
    parmesaa = [primerdiaaa, ultimodiaaa, 0, 'N']
    cur.execute("select * from VENTA_TOTAL_PER_PV(?, ?, ?, ?)", (parmesaa))
    ventamesaa = cur.fetchone()

    """DIFERENCIAS DE VENTA"""
    diferencia = ventames[0] - ventamesaa[0]
    diferenciap = format(ventames[0] / ventamesaa[0], '.1f')

    datos = {
        "venta":venta,
        "fecha":fecha,
        "now":now,
        "ventas":ventas,
        "total":total,
        "totaltransacciones":totaltransacciones,
        "ticket":ticket,
        "ventames":ventames,
        "ventamesaa":ventamesaa,
        "diferencia":diferencia,
        "diferenciap":diferenciap,
    }
    return render(request, "stats/dash.html", datos)

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
