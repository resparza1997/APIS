from django.contrib import admin
from .models import *

# Register your models here.

class InventarioAdmin(admin.ModelAdmin):
    list_display=("Producto", "Cantidad", "PrecioCliente", "PrecioProvedor")
    search_fields=("Producto",)

class ProbedorAdmin(admin.ModelAdmin):
    list_display=("Probedor", "Descripcion")
    search_fields=("Probedor",)

class TransaccionesClientesAdmin(admin.ModelAdmin):
    list_display=("Usuario", "Fecha", "Producto", "Cantidad", "CostoTotal")
    search_fields=("Usuario",)
    list_filter=("Fecha",)

class TransaccionesProbedoresAdmin(admin.ModelAdmin):
    list_display=("Usuario", "Probedor", "Fecha", "Producto", "Cantidad", "CostoTotal")
    search_fields=("Fecha",)

admin.site.register(Inventario, InventarioAdmin)
admin.site.register(Probedor, ProbedorAdmin)
admin.site.register(TransaccionesClientes, TransaccionesClientesAdmin)
admin.site.register(TransaccionesProbedores, TransaccionesProbedoresAdmin)