from django.contrib import admin
from .models import Almacen, Perfil

# Register your models here.
class AlmacenAdmin(admin.ModelAdmin):
    list_display = ("id", "numero", "nombre", "ciudad")


admin.site.register(Almacen, AlmacenAdmin)

class PerfilAdmin(admin.ModelAdmin):
    list_display = ("id", "user", "email")

admin.site.register(Perfil, PerfilAdmin)