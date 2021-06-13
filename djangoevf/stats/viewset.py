from rest_framework import viewsets
from .models import Almacen
from .serializer import AlmacenSerializer

class AlmacenViewSet(viewsets.ModelViewSet):
    queryset = Almacen.objects.all()
    serializer_class = AlmacenSerializer