from django.conf import settings
from django.db import models

# Create your models here.
class Perfil(models.Model):
    user = models.OneToOneField(settings.AUTH_USER_MODEL, on_delete=models.CASCADE)
    email = models.EmailField
    tipo = models.CharField(max_length=25)

    def __str__(self):
        return self.user

class Almacen(models.Model):
    numero = models.CharField(max_length=8)
    nombre = models.CharField(max_length=55)
    ciudad = models.CharField(max_length=25)

    def __str__(self):
        return self.nombre
    
