from django.contrib import admin
from .models import Alumno

@admin.register(Alumno)
class AlumnoAdmin(admin.ModelAdmin):
    list_display = ("apellidos", "nombres", "telefono", "fecha_pago", "fecha_vencimiento")
    search_fields = ("nombres", "apellidos", "telefono")
    ordering = ("apellidos",)
