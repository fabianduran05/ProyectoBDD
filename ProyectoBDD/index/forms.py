from django import forms 
from .models import *

# class RegistroParametrosForm(forms.Form):
#     nombre = forms.CharField(label="Nombre User", error_messages={
#         "required": "Debe seleccionar un piscina"
#     })

class RegistroParametrosForm(forms.ModelForm):
    class Meta:
        model = Mediciones
        fields = "__all__"
        labels={
            "oxigeno": "Oxígeno"
        }
        error_messages={
            "piscina": {
                "required": "Seleccione una piscina"
            },
            "oxigeno": {
                "required": "Ingrese el oxígeno"
            },
            "ph": {
                "required": "Ingrese el Ph"
            },
            "salinidad": {
                "required": "Ingrese la salinidad"
            }
        }

class RegistroPiscinaForm(forms.ModelForm):
    class Meta:
        model = Piscinas
        fields = "__all__"
        labels = {
            "ubicacion": "Ubicación"
        }
        error_messages={
            "nombre":{
                "required": "Ingrese un nombre",
                "unique": "Ya existe una piscina con este nombre"
            },
            "ubicacion":{
                "required": "Debe ingresar una ubicacion"
            }
        }
class RegistrosFechaForm(forms.Form):
    fecha_inicio = forms.DateField(label="Desde", input_formats=["%Y-%m-%d"], 
                                   widget=forms.TextInput(attrs={
            'placeholder': 'YYYY-MM-DD'
        }), error_messages={'required': 'Por favor, introduzca la fecha de inicio.'})
    fecha_final = forms.DateField(label="Hasta", input_formats=["%Y-%m-%d"],
                                  widget=forms.TextInput(attrs={
            'placeholder': 'YYYY-MM-DD'
        }), error_messages={'required': 'Por favor, introduzca la fecha final.'})

class ElegirPiscinaForm(forms.ModelForm):
    piscina = forms.ModelChoiceField(queryset=Piscinas.objects.all(), empty_label="Selecione una piscina", error_messages = {"required": "Seleccione una piscina"})

    class Meta:
        model = Piscinas
        fields = ["piscina"]
        
        