from django import forms
from .models import Alumno

class AlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = [
            "nombres",
            "apellidos",
            "telefono",
            "fecha_nacimiento",
            "fecha_pago",
            "meses_pagados",
        ]

        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
            "fecha_pago": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"]

        if not telefono.isdigit():
            raise forms.ValidationError("Ingresa un número telefónico válido.")

        if len(telefono) != 10:
            raise forms.ValidationError("Ingresa un número telefónico válido.")

        return telefono


class EditarAlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ["telefono", "fecha_nacimiento"]

        widgets = {
            "fecha_nacimiento": forms.DateInput(attrs={"type": "date"}),
        }

    def clean_telefono(self):
        telefono = self.cleaned_data["telefono"]

        if not telefono.isdigit():
            raise forms.ValidationError("Ingresa un número telefónico válido.")

        if len(telefono) != 10:
            raise forms.ValidationError("Ingresa un número telefónico válido.")

        return telefono
