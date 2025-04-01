# from django.urls import path
# from .views import lista_ingresos, lista_egresos

# urlpatterns = [
#     path('ingresos/', lista_ingresos, name='lista_ingresos'),
#     path('egresos/', lista_egresos, name='lista_egresos'),
# ]
from django.urls import path
from .views import (
    lista_ingresos, lista_egresos,
    crear_ingreso, editar_ingreso, eliminar_ingreso,
    crear_egreso, editar_egreso, eliminar_egreso, resumen_finanzas
)


urlpatterns = [
    # URLs para ingresos
    path('ingresos/', lista_ingresos, name='lista_ingresos'),
    path('ingresos/crear/', crear_ingreso, name='crear_ingreso'),
    path('ingresos/editar/<int:pk>/', editar_ingreso, name='editar_ingreso'),
    path('ingresos/eliminar/<int:pk>/', eliminar_ingreso, name='eliminar_ingreso'),

    # URLs para egresos
    path('egresos/', lista_egresos, name='lista_egresos'),
    path('egresos/crear/', crear_egreso, name='crear_egreso'),
    path('egresos/editar/<int:pk>/', editar_egreso, name='editar_egreso'),
    path('egresos/eliminar/<int:pk>/', eliminar_egreso, name='eliminar_egreso'),
    path('resumen/', resumen_finanzas, name='resumen_finanzas'),
]