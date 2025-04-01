# from django.urls import path
# from .views import lista_cotizaciones, detalle_cotizacion


# urlpatterns = [
#     path('', lista_cotizaciones, name='lista_cotizaciones'),
#     path('<int:cotizacion_id>/', detalle_cotizacion, name='detalle_cotizacion'),

# ]

# cotizaciones/urls.py
from django.urls import path
from .views import (
    lista_cotizaciones, detalle_cotizacion,
    crear_cotizacion, editar_cotizacion, eliminar_cotizacion,
    lista_clientes, crear_cliente, editar_cliente, eliminar_cliente
)


urlpatterns = [
    path('', lista_cotizaciones, name='lista_cotizaciones'),
    path('<int:cotizacion_id>/', detalle_cotizacion, name='detalle_cotizacion'),
    path('crear/', crear_cotizacion, name='crear_cotizacion'),
    path('editar/<int:cotizacion_id>/', editar_cotizacion, name='editar_cotizacion'),
    path('eliminar/<int:cotizacion_id>/', eliminar_cotizacion, name='eliminar_cotizacion'),
    path('clientes/', lista_clientes, name='lista_clientes'),
    path('clientes/crear/', crear_cliente, name='crear_cliente'),
    path('clientes/editar/<int:cliente_id>/', editar_cliente, name='editar_cliente'),
    path('clientes/eliminar/<int:cliente_id>/', eliminar_cliente, name='eliminar_cliente'),
]