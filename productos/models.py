from django.db import models
from django.utils import timezone


class Producto(models.Model):
    id = models.CharField(primary_key=True, max_length=50, unique=True)
    nombre = models.CharField(max_length=100, unique=True)
    stock_actual = models.PositiveIntegerField(default=0)
    activo = models.BooleanField(default=True)

    def __str__(self):
        return self.nombre


class VentaProducto(models.Model):
    producto = models.ForeignKey(
        Producto,
        on_delete=models.CASCADE,
        related_name="ventas"
    )
    cantidad = models.PositiveIntegerField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)
    fecha_venta = models.DateField(default=timezone.localdate)

    def __str__(self):
        return f"{self.producto.nombre} - {self.fecha_venta} - ${self.monto}"
