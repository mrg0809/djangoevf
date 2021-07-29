from datetime import datetime, timedelta, timezone
import firebirdsql

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



def consultaTallas(modelo):
    partallas = [modelo.upper(), 19]
    cur.execute("select * from VT_EXIS_MODELO_TALLAS_ALM(?, ?)",(partallas))
    datos = cur.fetchall()
    tallas = []
    
    for x in datos:
        tallas.append(x[6])
    
    settallas = set(tallas)
    tallas = list(settallas)
    tallas.sort()
    return tallas



def TallasAlmacen(modelo, almacen):
    parametros = [modelo.upper(), almacen]
    cur.execute("select TALLA, EXISTENCIA from VT_EXIS_MODELO_TALLAS_ALM(?, ?) order by TALLA asc",(parametros))
    datos = cur.fetchall()
    return datos


