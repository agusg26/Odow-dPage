from django import forms
from Catalogo.models import Cerveza

class CervezaForm(forms.ModelForm):
    class Meta:
        model = Cerveza
        fields = ['nombre', 'descripcion', 'estilo', 'porcentaje_alcohol', 'ibu']