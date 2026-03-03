from datetime import date, timedelta
from django.shortcuts import render, get_object_or_404, redirect
from .models import Alumno
from .forms import *
from django.contrib.auth.decorators import login_required
from django.utils import timezone
from datetime import timedelta
from .models import Pago
from django.db.models import Sum

@login_required
def menu_principal(request):
    return render(request, "menu.html")

@login_required
def registrar_alumno(request):
    if request.method == "POST":
        form = AlumnoForm(request.POST)
        if form.is_valid():
            alumno = form.save(commit=False)

            monto = form.cleaned_data["monto"]

            alumno.fecha_vencimiento = alumno.fecha_pago + timedelta(days=30 * alumno.meses_pagados)
            alumno.save()

            # 🔥 Crear primer pago
            Pago.objects.create(
                alumno=alumno,
                fecha_pago=alumno.fecha_pago,
                meses_pagados=alumno.meses_pagados,
                fecha_inicio=alumno.fecha_pago,
                fecha_fin=alumno.fecha_vencimiento,
                monto=monto
            )

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

    if request.method == "POST":
        form = EditarAlumnoForm(request.POST, instance=alumno)

        if form.is_valid():
            form.save()   # NO controlamos fechas aquí
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
        meses = int(request.POST.get("meses_pagados", 1))
        monto = float(request.POST.get("monto", 0))

        if alumno.fecha_vencimiento >= hoy:
            fecha_inicio = alumno.fecha_vencimiento
            nueva_fecha = alumno.fecha_vencimiento + timedelta(days=30 * meses)
        else:
            fecha_inicio = hoy
            nueva_fecha = hoy + timedelta(days=30 * meses)

        Pago.objects.create(
            alumno=alumno,
            fecha_pago=hoy,
            meses_pagados=meses,
            fecha_inicio=fecha_inicio,
            fecha_fin=nueva_fecha,
            monto=monto
        )

        # Actualizar estado actual del alumno
        alumno.fecha_pago = hoy
        alumno.meses_pagados = meses
        alumno.fecha_vencimiento = nueva_fecha
        alumno.save()

        return redirect("lista_renovar")

    return render(request, "renovar_membresia.html", {"alumno": alumno})


@login_required
def corte_caja(request):

    pagos = None
    total = None
    fecha_inicio = None
    fecha_fin = None

    if request.method == "POST":
        fecha_inicio_str = request.POST.get("fecha_inicio")
        fecha_fin_str = request.POST.get("fecha_fin")

        from datetime import datetime
        fecha_inicio = datetime.strptime(fecha_inicio_str, "%Y-%m-%d").date()
        fecha_fin = datetime.strptime(fecha_fin_str, "%Y-%m-%d").date()

        pagos = Pago.objects.filter(
            fecha_pago__range=[fecha_inicio, fecha_fin]
        )

        total = sum(p.monto for p in pagos)

    return render(request, "corte_caja.html", {
        "pagos": pagos,
        "total": total,
        "fecha_inicio": fecha_inicio,
        "fecha_fin": fecha_fin,
    })




