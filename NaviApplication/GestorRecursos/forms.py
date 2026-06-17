from django import forms
from .models import GestorRecursos
from django.contrib.auth.models import User
from .models import Recurso
from .choices import TIPO_CHOICES, SUBTIPO_CHOICES, TIPO_SUBTIPO_MAP
from GestorNavios.models import Puerto  # Importa tu modelo Puerto

class RecursoForm(forms.ModelForm):
    tipo = forms.ChoiceField(choices=TIPO_CHOICES)
    subtipo = forms.ChoiceField(choices=SUBTIPO_CHOICES, required=False)

    puertos_disponibles = forms.ModelMultipleChoiceField(
        queryset=Puerto.objects.all(),
        widget=forms.CheckboxSelectMultiple,
        required=False,
        label="Puertos disponibles"
    )

    class Meta:
        model = Recurso
        fields = ['nombre', 'precio', 'descripcion', 'imagen', 'tipo', 'subtipo', 'puertos_disponibles']

    def clean(self):
        cleaned_data = super().clean()
        tipo = cleaned_data.get('tipo')
        subtipo = cleaned_data.get('subtipo')

        if tipo and subtipo:
            subtipo_validos = TIPO_SUBTIPO_MAP.get(tipo, [])
            if subtipo not in subtipo_validos:
                raise forms.ValidationError(
                    f"El subtipo '{subtipo}' no es válido para el tipo '{tipo}'."
                )
            

class PerfilForm(forms.ModelForm):
    username = forms.CharField(max_length=150, required=True)  # Campo para el nombre de usuario

    class Meta:
        model = GestorRecursos
        fields = ['correo', 'telefono', 'direccion', 'descripcion']

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        if self.instance and self.instance.user:
            self.fields['username'].initial = self.instance.user.username  # Mostrar el nombre de usuario actual

    def save(self, commit=True):
        gestor = super().save(commit=False)
        gestor.user.username = self.cleaned_data['username']  # Guardar cambios en el usuario
        if commit:
            gestor.user.save()
            gestor.save()
        return gestor
