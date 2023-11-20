from django import forms
from .models import *

class ClaseForm(forms.ModelForm):
    class Meta:
        model = Clase
        fields = ('nombre', 'descripcion', 'nivel', 'instructor', 'requisitos', 'precio', 'horario', 'duracion', 'ubicacion', 'cuposMaximo', 'cuposActual', 'imagen')