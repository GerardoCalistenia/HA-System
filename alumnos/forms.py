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

class EditarAlumnoForm(forms.ModelForm):
    class Meta:
        model = Alumno
        fields = ['nombres', 'apellidos', 'telefono', 'fecha_nacimiento', 'fecha_pago', 'meses_pagados']

        widgets = {
            'nombres': forms.TextInput(attrs={'readonly': 'readonly'}),
            'apellidos': forms.TextInput(attrs={'readonly': 'readonly'}),
        }