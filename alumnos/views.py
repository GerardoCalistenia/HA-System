from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from .models import Alumno
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta

@login_required
def menu_principal(request):
    return render(request, "menu.html")

@login_required
def registrar_alumno(request):
    if request.method == "POST":
        form = AlumnoForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect("menu_principal")
    else:
        form = AlumnoForm()

    return render(request, "registrar_alumno.html", {"form": form})

@login_required
def lista_alumnos(request):
    alumnos = Alumno.objects.all().order_by("apellidos", "nombres")
    return render(request, "lista_alumnos.html", {"alumnos": alumnos})

@login_required
def editar_alumno(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)
    hoy = timezone.localdate()

    if request.method == "POST":
        form = EditarAlumnoForm(request.POST, instance=alumno)

        if form.is_valid():
            # Obtenemos valores modificados ANTES de guardar
            nuevo_pago = form.cleaned_data["fecha_pago"]

            # CASO 1: Si la nueva fecha de pago es mayor a hoy → se considera pago anticipado
            if alumno.fecha_vencimiento >= hoy and nuevo_pago > alumno.fecha_pago:
                # Acumular días desde su vencimiento actual
                nueva_vencimiento = alumno.fecha_vencimiento + timedelta(days=30)

            # CASO 2: Si ya estaba vencido → reset desde nueva fecha de pago
            elif alumno.fecha_vencimiento < hoy:
                nueva_vencimiento = nuevo_pago + timedelta(days=30)

            # CASO 3: Solo corrección de fecha, no debe resetear días
            else:
                dias_restantes = (alumno.fecha_vencimiento - alumno.fecha_pago).days
                nueva_vencimiento = nuevo_pago + timedelta(days=dias_restantes)

            # Aplicar los cambios manualmente sin perder acumulación
            alumno.fecha_pago = nuevo_pago
            alumno.telefono = form.cleaned_data["telefono"]
            alumno.fecha_nacimiento = form.cleaned_data["fecha_nacimiento"]
            alumno.fecha_vencimiento = nueva_vencimiento

            alumno.save()  # Guardar sin recalcular mal

            return redirect("lista_alumnos")

    else:
        form = EditarAlumnoForm(instance=alumno)

    return render(request, "editar_alumno.html", {"form": form, "alumno": alumno})

@login_required
def eliminar_alumno(request, alumno_id):
    alumno = Alumno.objects.get(id=alumno_id)
    alumno.delete()
    return redirect("lista_alumnos")


@login_required
def alumnos_proximos_vencer(request):
    hoy = timezone.localdate()
    limite = hoy + timedelta(days=5)

    alumnos = Alumno.objects.filter(
        fecha_vencimiento__range=[hoy, limite]
    ).order_by("fecha_vencimiento")

    return render(request, "alumnos_proximos_vencer.html", {"alumnos": alumnos})

@login_required
def alumnos_vencidos(request):
    hoy = timezone.localdate()

    alumnos = Alumno.objects.filter(
        fecha_vencimiento__lt=hoy
    ).order_by("fecha_vencimiento")

    return render(request, "alumnos_vencidos.html", {"alumnos": alumnos})

@login_required
def lista_renovar(request):
    alumnos = Alumno.objects.all().order_by("apellidos", "nombres")
    return render(request, "lista_renovar.html", {"alumnos": alumnos})

@login_required
def renovar_membresia(request, alumno_id):
    alumno = get_object_or_404(Alumno, id=alumno_id)

    hoy = timezone.localdate()

    if request.method == "POST":
        meses = int(request.POST.get("meses", 1))

        # Si aún no vence → acumular desde la fecha actual de vencimiento
        if alumno.fecha_vencimiento >= hoy:
            nueva_fecha = alumno.fecha_vencimiento + timedelta(days=30 * meses)
        else:
            # Si ya venció → reiniciar desde hoy
            nueva_fecha = hoy + timedelta(days=30 * meses)

        # Actualizar solo lo necesario
        alumno.fecha_pago = hoy
        alumno.meses_pagados = meses

        # ⚠️ Asignar aquí ANTES del save,
        # porque el save del modelo lo recalcularía mal
        alumno.fecha_vencimiento = nueva_fecha

        # Guardar sin que el save del modelo te destruya la fecha nueva
        alumno.save()

        return redirect("lista_renovar")

    return render(request, "renovar_membresia.html", {"alumno": alumno})


