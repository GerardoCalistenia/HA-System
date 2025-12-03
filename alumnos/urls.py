from . import views
from django.urls import path
from django.contrib.auth import views as auth_views

urlpatterns = [
    path('login/', auth_views.LoginView.as_view(template_name='login.html'), name='login'),
    path('logout/', auth_views.LogoutView.as_view(next_page='login'), name='logout'),
    path('', views.menu_principal, name='menu_principal'),
    path("registrar/", views.registrar_alumno, name="registrar_alumno"),
    path("lista/", views.lista_alumnos, name="lista_alumnos"),
    path("editar/<str:alumno_id>/", views.editar_alumno, name="editar_alumno"),
    path("eliminar/<str:alumno_id>/", views.eliminar_alumno, name="eliminar_alumno"),
    path("proximos/", views.alumnos_proximos_vencer, name="alumnos_proximos_vencer"),
    path("vencidos/", views.alumnos_vencidos, name="alumnos_vencidos"),
    path("renovar/<str:alumno_id>/", views.renovar_membresia, name="renovar_membresia"),
    path("renovar/", views.lista_renovar, name="lista_renovar"),
]
