from django.db import models
from django.utils import timezone
import unicodedata
import re


def limpiar_campo(texto):
    if not texto:
        return ""

    # Quitar acentos
    texto = unicodedata.normalize("NFKD", texto).encode("ascii", "ignore").decode("ascii")

    # Quitar puntos y caracteres innecesarios
    texto = re.sub(r"[^a-zA-Z0-9\s]", "", texto)

    # Quitar espacios extras
    texto = re.sub(r"\s+", " ", texto).strip()

    # Poner todo en MAYÚSCULAS
    texto = texto.upper()

    return texto


class Alumno(models.Model):
    id = models.CharField(primary_key=True, max_length=255, unique=True)

    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=120)
    telefono = models.CharField(max_length=20)

    fecha_nacimiento = models.DateField()

    fecha_pago = models.DateField(default=timezone.now)
    meses_pagados = models.PositiveIntegerField(default=1)

    fecha_vencimiento = models.DateField()

    def save(self, *args, **kwargs):

        # Limpiar antes de guardar
        self.nombres = limpiar_campo(self.nombres)
        self.apellidos = limpiar_campo(self.apellidos)

        # Generar ID seguro (sin acentos, sin espacios dobles)
        ap = self.apellidos.replace(" ", "_").lower()
        nom = self.nombres.replace(" ", "_").lower()
        self.id = f"{ap}_{nom}"

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"
    
class Pago(models.Model):
    alumno = models.ForeignKey(Alumno, on_delete=models.CASCADE, related_name="pagos")
    fecha_pago = models.DateField()
    meses_pagados = models.PositiveIntegerField()
    fecha_inicio = models.DateField()
    fecha_fin = models.DateField()
    monto = models.DecimalField(max_digits=10, decimal_places=2)

    def __str__(self):
        return f"{self.alumno} - {self.fecha_pago} - ${self.monto}"

