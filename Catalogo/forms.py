from django import forms
from Catalogo.models import Cerveza, TipoServicio, Chopera, Barril, Servicio

class CervezaForm(forms.ModelForm):
    class Meta:
        model = Cerveza
        fields = ['nombre', 'descripcion', 'estilo', 'porcentaje_alcohol', 'ibu']

class VentaForm(forms.Form):
    #toma un modelo y muestra una lista desplegable de un atributo del mismo, luego setea el campo en vacio.
    barril = forms.ModelChoiceField(queryset=Barril.objects.none(), label="Formato (Litros)")
    cantidad = forms.IntegerField(min_value=1, label="Cantidad")

    #es el metodo constructor. Le pasa una cerveza por parametro para filtrar barriles solo de ese estilo
    def __init__(self, cerveza, *args, **kwargs):
        super().__init__(*args, **kwargs)
        #toma el campo del form y filtra los barriles para que se muestren solo de ese estilo y con stock > 0
        self.fields['barril'].queryset = Barril.objects.filter(cerveza=cerveza, stock__gt=0)

class ServicioForm(forms.ModelForm):
    class Meta:
        model = Servicio
        fields = ['nombre', 'descripcion', 'tipo', 'precio', 'foto']
        widgets = {
            'descripcion': forms.Textarea(attrs={'rows': 4}),
        }