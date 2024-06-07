from django import forms
from .models import Producto

class ProductoForm(forms.ModelForm):
    class Meta:
        model = Producto
        fields = ['nombre', 'precio', 'cantidad']

class CSVUploadForm(forms.Form):
    csv_file = forms.FileField(label='Seleccionar archivo CSV')
