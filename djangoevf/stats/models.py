from django.db import models

# Create your models here.
class Almacen(models.Model):
    numero = models.CharField(max_length=8)
    nombre = models.CharField(max_length=55)
    ciudad = models.CharField(max_length=25)

    def __str__(self):
        return self.nombre
    
