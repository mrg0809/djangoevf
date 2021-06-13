from django.contrib import admin
from .models import Almacen

# Register your models here.
class AlmacenAdmin(admin.ModelAdmin):
    list_display = ("id", "numero", "nombre", "ciudad")


admin.site.register(Almacen, AlmacenAdmin)