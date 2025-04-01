from django import forms
from django.forms import inlineformset_factory
from .models import Cotizacion, Cliente, ItemCotizacion
from django.core.exceptions import ValidationError
# import phonenumbers

# Formulario para el modelo Cliente
class ClienteForm(forms.ModelForm):

    class Meta:
        model = Cliente
        fields = ['nombre', 'email', 'telefono', 'direccion']  # Agregar dirección
        widgets = {
            'direccion': forms.Textarea(attrs={'rows': 3}),  # Hacer el campo de dirección más grande
        }

# Formulario para el modelo Cotizacion
class CotizacionForm(forms.ModelForm):
    class Meta:
        model = Cotizacion
        fields = [
            'cliente', 'fecha_vencimiento', 'condiciones_pago',
            'estado', 'subtotal', 'impuestos', 'descuentos', 'total', 'condiciones_adicionales',
            'porcentaje_descuentos','porcentaje_impuestos'
        ]
        widgets = {
            'fecha_vencimiento': forms.DateInput(attrs={'type': 'date'}),  # Usar un date picker
            'condiciones_pago': forms.TextInput(),  # Campo de texto simple
            'condiciones_adicionales': forms.Textarea(attrs={'rows': 3}),  # Área de texto para condiciones
        }
    
    porcentaje_impuestos = forms.DecimalField(
        label="Impuestos (%)",
        max_digits=5,
        decimal_places=2,
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    porcentaje_descuentos = forms.DecimalField(
        label="Descuentos (%)",
        max_digits=5,
        decimal_places=2,
        required=False,
        initial=0,
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )


    def __init__(self, *args, **kwargs):
        # Obtener el usuario pasado como argumento
        self.usuario = kwargs.pop('usuario', None)
        super().__init__(*args, **kwargs)
        # Filtrar clientes por el usuario actual
        if self.usuario:
            self.fields['cliente'].queryset = Cliente.objects.filter(usuario=self.usuario)
        self.fields['subtotal'].required = False
        self.fields['impuestos'].required = False
        self.fields['descuentos'].required = False
        self.fields['total'].required = False

# Formulario para el modelo ItemCotizacion
class ItemCotizacionForm(forms.ModelForm):
    class Meta:
        model = ItemCotizacion
        fields = ['descripcion', 'cantidad', 'unidad_medida', 'precio_unitario']  # Agregar unidad_medida
        widgets = {
            'descripcion': forms.TextInput(attrs={'placeholder': 'Descripción del ítem'}),
            'cantidad': forms.NumberInput(attrs={'placeholder': 'Cantidad'}),
            'unidad_medida': forms.TextInput(attrs={'placeholder': 'Unidad de medida'}),
            'precio_unitario': forms.NumberInput(attrs={'placeholder': 'Precio unitario'}),
        }


# Formset para los ítems de la cotización
ItemCotizacionFormSet = inlineformset_factory(
    Cotizacion,  # Modelo principal
    ItemCotizacion,  # Modelo relacionado
    form=ItemCotizacionForm,  # Formulario para los ítems
    extra=1,  # Número de formularios vacíos para mostrar
    can_delete=True,  # Permite eliminar ítems
)