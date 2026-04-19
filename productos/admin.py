from django.contrib import admin
from .models import Producto, VentaProducto


@admin.register(Producto)
class ProductoAdmin(admin.ModelAdmin):
    list_display = ("id", "nombre", "stock_actual", "activo")
    search_fields = ("id", "nombre")
    list_filter = ("activo",)
    ordering = ("nombre",)


@admin.register(VentaProducto)
class VentaProductoAdmin(admin.ModelAdmin):
    list_display = ("producto", "cantidad", "monto", "fecha_venta")
    search_fields = ("producto__nombre", "producto__id")
    list_filter = ("fecha_venta",)
    ordering = ("-fecha_venta",)

    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False
