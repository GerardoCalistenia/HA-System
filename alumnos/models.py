from django.db import models
from django.utils import timezone
from datetime import timedelta

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
        # Generar ID seguro y limpio
        ap = self.apellidos.strip().replace(" ", "_")
        nom = self.nombres.strip().replace(" ", "_")
        self.id = f"{ap}_{nom}".lower()

        super().save(*args, **kwargs)

    def __str__(self):
        return f"{self.apellidos}, {self.nombres}"
