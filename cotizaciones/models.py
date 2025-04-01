from django.db import models
from django.contrib.auth.models import User
from django.utils import timezone

class Cliente(models.Model):
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=255)
    direccion = models.TextField(blank=True, null=True)  # Nueva dirección del cliente
    telefono = models.CharField(max_length=15, blank=True, null=True)
    email = models.EmailField(unique=True)

    def __str__(self):
        return self.nombre

# class Cotizacion(models.Model):
#     ESTADO_CHOICES = [
#         ('pendiente', 'Pendiente'),
#         ('aceptada', 'Aceptada'),
#         ('rechazada', 'Rechazada'),
#     ]

#     usuario = models.ForeignKey(User, on_delete=models.CASCADE)
#     cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
#     fecha_emision = models.DateField(auto_now_add=True)  # Fecha de emisión
#     fecha_vencimiento = models.DateField(default=timezone.now)  # Fecha de vencimiento
#     condiciones_pago = models.CharField(max_length=255, blank=True, null=True)  # Condiciones de pago
#     estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
#     subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Subtotal
#     impuestos = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Impuestos
#     descuentos = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Descuentos
#     total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Total
#     condiciones_adicionales = models.TextField(blank=True, null=True)  # Condiciones adicionales

#     def calcular_total(self):
#         self.subtotal = sum(item.subtotal() for item in self.items.all())
#         self.total = self.subtotal + self.impuestos - self.descuentos
#         self.save()

#     def __str__(self):
#         return f"Cotización #{self.id} - {self.cliente.nombre} ({self.estado})"
class Cotizacion(models.Model):
    ESTADO_CHOICES = [
        ('pendiente', 'Pendiente'),
        ('aceptada', 'Aceptada'),
        ('rechazada', 'Rechazada'),
    ]

    usuario = models.ForeignKey(User, on_delete=models.CASCADE)
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    fecha_emision = models.DateField(auto_now_add=True)  # Fecha de emisión
    fecha_vencimiento = models.DateField(default=timezone.now)  # Fecha de vencimiento
    condiciones_pago = models.CharField(max_length=255, blank=True, null=True)  # Condiciones de pago
    estado = models.CharField(max_length=10, choices=ESTADO_CHOICES, default='pendiente')
    subtotal = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Subtotal
    impuestos = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Impuestos
    descuentos = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Descuentos
    total = models.DecimalField(max_digits=10, decimal_places=2, default=0)  # Total
    condiciones_adicionales = models.TextField(blank=True, null=True)  # Condiciones adicionales
    porcentaje_impuestos = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Porcentaje de impuestos
    porcentaje_descuentos = models.DecimalField(max_digits=5, decimal_places=2, default=0)  # Porcentaje de descuentos

    def calcular_total(self):
        # Calcular el subtotal sumando los ítems
        self.subtotal = sum(item.subtotal() for item in self.items.all())

        # Calcular impuestos y descuentos en función de los porcentajes
        self.impuestos = (self.subtotal * self.porcentaje_impuestos) / 100
        self.descuentos = (self.subtotal * self.porcentaje_descuentos) / 100

        # Calcular el total
        self.total = self.subtotal + self.impuestos - self.descuentos

        # Guardar los cambios
        self.save()

    def __str__(self):
        return f"Cotización #{self.id} - {self.cliente.nombre} ({self.estado})"

class ItemCotizacion(models.Model):
    cotizacion = models.ForeignKey(Cotizacion, on_delete=models.CASCADE, related_name="items")
    descripcion = models.CharField(max_length=255)
    cantidad = models.PositiveIntegerField(default=1)
    unidad_medida = models.CharField(max_length=50, blank=True, null=True)  # Unidad de medida
    precio_unitario = models.DecimalField(max_digits=10, decimal_places=2)

    def subtotal(self):
        return self.cantidad * self.precio_unitario

    def __str__(self):
        return f"{self.descripcion} - {self.cantidad} x {self.precio_unitario}"
