from django.contrib import messages
from django.contrib.auth.decorators import login_required
from django.db import transaction
from django.db.models import Sum
from django.http import HttpResponseBadRequest
from django.shortcuts import get_object_or_404, redirect, render
from django.utils import timezone

from .forms import VentaProductoForm
from .models import Producto, VentaProducto


def construir_productos_con_totales(producto_con_error_id=None, form_con_error=None):
    productos = Producto.objects.filter(activo=True).prefetch_related("ventas").order_by("nombre")
    productos_con_totales = []

    for producto in productos:
        total_vendido = producto.ventas.aggregate(total=Sum("monto"))["total"] or 0
        historial = producto.ventas.all().order_by("-fecha_venta", "-id")

        productos_con_totales.append({
            "producto": producto,
            "total_vendido": total_vendido,
            "historial": historial,
            "form": form_con_error if producto.id == producto_con_error_id else VentaProductoForm(),
        })

    return productos_con_totales


@login_required
def lista_productos(request):
    return render(request, "productos/lista_productos.html", {
        "productos_con_totales": construir_productos_con_totales(),
    })


@login_required
@transaction.atomic
def vender_producto(request, producto_id):
    if request.method != "POST":
        return HttpResponseBadRequest("Metodo no permitido.")

    producto = get_object_or_404(Producto, id=producto_id, activo=True)
    form = VentaProductoForm(request.POST)

    if not form.is_valid():
        messages.error(request, "No se pudo registrar la venta. Revisa los datos capturados.")
        return render(request, "productos/lista_productos.html", {
            "productos_con_totales": construir_productos_con_totales(producto.id, form),
        }, status=400)

    cantidad = form.cleaned_data["cantidad"]
    monto = form.cleaned_data["monto"]

    if cantidad > producto.stock_actual:
        form.add_error("cantidad", "No hay suficiente inventario disponible.")
        messages.error(request, "No se pudo registrar la venta porque el inventario es insuficiente.")
        return render(request, "productos/lista_productos.html", {
            "productos_con_totales": construir_productos_con_totales(producto.id, form),
        }, status=400)

    VentaProducto.objects.create(
        producto=producto,
        cantidad=cantidad,
        monto=monto,
        fecha_venta=timezone.localdate(),
    )

    producto.stock_actual -= cantidad
    producto.save()

    messages.success(
        request,
        f"Venta registrada correctamente para {producto.nombre}. Stock restante: {producto.stock_actual}."
    )
    return redirect("lista_productos")

