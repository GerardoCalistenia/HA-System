from decimal import Decimal

from django.contrib.auth.models import User
from django.test import TestCase
from django.urls import reverse
from django.utils import timezone

from .models import Producto, VentaProducto


class ProductosViewsTests(TestCase):
    def setUp(self):
        self.user = User.objects.create_user(
            username="tester",
            password="pass12345",
        )
        self.producto = Producto.objects.create(
            id="playera_negra_m",
            nombre="Playera negra talla M",
            stock_actual=10,
            activo=True,
        )

    def test_lista_productos_requires_login(self):
        response = self.client.get(reverse("lista_productos"))

        self.assertEqual(response.status_code, 302)
        self.assertIn("/login/", response.url)

    def test_lista_productos_muestra_productos_activos(self):
        Producto.objects.create(
            id="playera_inactiva",
            nombre="Playera inactiva",
            stock_actual=5,
            activo=False,
        )
        self.client.login(username="tester", password="pass12345")

        response = self.client.get(reverse("lista_productos"))

        self.assertEqual(response.status_code, 200)
        self.assertContains(response, "Playera negra talla M")
        self.assertNotContains(response, "Playera inactiva")

    def test_vender_producto_registra_venta_y_descuenta_stock(self):
        self.client.login(username="tester", password="pass12345")

        response = self.client.post(
            reverse("vender_producto", args=[self.producto.id]),
            {
                "cantidad": 3,
                "monto": "450.00",
            },
            follow=True,
        )

        self.producto.refresh_from_db()
        venta = VentaProducto.objects.get(producto=self.producto)

        self.assertEqual(response.status_code, 200)
        self.assertEqual(self.producto.stock_actual, 7)
        self.assertEqual(venta.cantidad, 3)
        self.assertEqual(venta.monto, Decimal("450.00"))
        self.assertEqual(venta.fecha_venta, timezone.localdate())
        self.assertContains(response, "Venta registrada correctamente")

    def test_vender_producto_rechaza_stock_insuficiente(self):
        self.client.login(username="tester", password="pass12345")

        response = self.client.post(
            reverse("vender_producto", args=[self.producto.id]),
            {
                "cantidad": 15,
                "monto": "900.00",
            },
        )

        self.producto.refresh_from_db()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(VentaProducto.objects.count(), 0)
        self.assertEqual(self.producto.stock_actual, 10)
        self.assertIn("inventario es insuficiente", response.content.decode())
        self.assertIn("No hay suficiente inventario disponible.", response.content.decode())

    def test_vender_producto_rechaza_datos_invalidos(self):
        self.client.login(username="tester", password="pass12345")

        response = self.client.post(
            reverse("vender_producto", args=[self.producto.id]),
            {
                "cantidad": 0,
                "monto": "0",
            },
        )

        self.producto.refresh_from_db()

        self.assertEqual(response.status_code, 400)
        self.assertEqual(VentaProducto.objects.count(), 0)
        self.assertEqual(self.producto.stock_actual, 10)
        self.assertIn(
            "No se pudo registrar la venta. Revisa los datos capturados.",
            response.content.decode(),
        )

    def test_vender_producto_get_no_permitido(self):
        self.client.login(username="tester", password="pass12345")

        response = self.client.get(reverse("vender_producto", args=[self.producto.id]))

        self.assertEqual(response.status_code, 400)
        self.assertIn("Metodo no permitido.", response.content.decode())
