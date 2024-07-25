from django.urls import path
from . import views

urlpatterns = [
    path("", views.index, name="registrar-parametros"),
    path("registrar-piscina", views.registro_piscina, name="registrar-piscina"),
    path("registros-recientes", views.registros_recientes, name="registros-recientes"),
    path("lista-registros/", views.lista_registros, name="lista-registros"),
    path("lista-fuera-control/", views.lista_fuera_control, name="lista-fuera-control"),
    path("registros-fuera-control", views.registros_fuera_control, name="registros-fuera-control"),
    path("actualizar/<int:pk>", views.actualizar, name="actualizar"),
    path("eliminar-registro/<int:pk>", views.eliminar_registro, name="eliminar-registro"),
    path("registros-fechas", views.registros_fecha, name="registros-fechas"),
    path("lista-registro-fechas/", views.lista_registros_fechas, name="lista-registros-fechas"),
    path("mostrar_lista_fechas", views.mostrar_lista_fechas, name="mostrar-lista-fecha"),
    path("elegir-piscina", views.elegir_piscina, name="elegir-piscina"),
    path("mostrar-lista-piscina", views.mostrar_lista_piscina, name="mostrar-lista-piscina"),
    path("lista-piscina/", views.lista_registros_piscina, name="lista-piscina"),
    path("piscinas-todas/", views.lista_piscinas, name="piscinas-todas"),
    path("piscinas-datatable", views.piscinas, name="piscinas-datatable"),
    path("actualizar-piscina/<int:pk>", views.actualizar_piscina, name="actualizar-piscina"),
    path("eliminar-piscina/<int:pk>", views.eliminar_piscina, name="eliminar-piscina"),
    path("graficos", views.graficos, name="graficos"),
    path("get-chart/", views.get_chart, name="get-chart")
]
