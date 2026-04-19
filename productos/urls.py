from django.urls import path
from . import views

urlpatterns = [
    path("", views.lista_productos, name="lista_productos"),
    path("vender/<str:producto_id>/", views.vender_producto, name="vender_producto"),
]
