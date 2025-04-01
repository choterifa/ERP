from django import forms
from .models import Ingreso, Egreso

class IngresoForm(forms.ModelForm):
    class Meta:
        model = Ingreso
        fields = ['monto', 'descripcion']

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto <= 0:
            raise forms.ValidationError("El monto debe ser mayor que cero.")
        return monto    

class EgresoForm(forms.ModelForm):
    class Meta:
        model = Egreso
        fields = ['monto', 'descripcion']

    def clean_monto(self):
        monto = self.cleaned_data.get('monto')
        if monto <= 0:
            raise forms.ValidationError("El monto debe ser mayor que cero.")
        return monto    