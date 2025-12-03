from django.db import models
from django.utils import timezone
from datetime import timedelta

class Alumno(models.Model):
    # Identificador único basado en nombre completo
    # Evita duplicados
    id = models.CharField(primary_key=True, max_length=255, unique=True)

    nombres = models.CharField(max_length=100)
    apellidos = models.CharField(max_length=120)
    telefono = models.CharField(max_length=20)

    fecha_nacimiento = models.DateField()

    fecha_pago = models.DateField(default=timezone.now)
    meses_pagados = models.PositiveIntegerField(default=1)

    fecha_vencimiento = models.DateField()

def save(self, *args, **kwargs):
    # ID basado en nombre
    self.id = f"{self.apellidos.strip().replace(' ', '_')}_{self.nombres.strip().replace(' ', '_')}".lower()

    # Solo recalcular si NO viene definida desde la vista
    if not self.fecha_vencimiento:
        self.fecha_vencimiento = self.fecha_pago + timedelta(days=30 * self.meses_pagados)

    super().save(*args, **kwargs)


    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"
