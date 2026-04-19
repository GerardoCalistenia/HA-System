from decimal import Decimal

from django import forms


class VentaProductoForm(forms.Form):
    cantidad = forms.IntegerField(
        min_value=1,
        widget=forms.NumberInput(attrs={
            "min": "1",
            "placeholder": "Cantidad de productos",
        })
    )
    monto = forms.DecimalField(
        max_digits=10,
        decimal_places=2,
        min_value=Decimal("0.01"),
        widget=forms.NumberInput(attrs={
            "min": "0.01",
            "step": "0.01",
            "placeholder": "Monto a pagar",
        })
    )
