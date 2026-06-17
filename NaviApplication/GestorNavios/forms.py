from django import forms
from .models import Navio

class NavioForm(forms.ModelForm):
    class Meta:
        model = Navio
        fields = ['imoNumero', 'nombre', 'capacidad', 'eslora', 'manga']
        widgets = {
            'imoNumero': forms.NumberInput(attrs={
                'class': 'form-control',
                'placeholder': 'Número IMO de 7 dígitos'
            }),
            'nombre': forms.TextInput(attrs={
                'class': 'form-control',
                'placeholder': 'Nombre del navío'
            }),
            'capacidad': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Capacidad en toneladas'
            }),
            'eslora': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Eslora en metros'
            }),
            'manga': forms.NumberInput(attrs={
                'class': 'form-control',
                'step': '0.01',
                'placeholder': 'Manga en metros'
            }),
        }
    def clean(self):
        cleaned_data = super().clean()
        imo = cleaned_data.get('imoNumero')
        
        if imo:
            # Verificamos si ya existe otro navío con el mismo IMO
            query = Navio.objects.filter(imoNumero=imo)
            
            # Si estamos editando un navío existente (tiene instancia)
            if self.instance and self.instance.pk:
                # Excluimos el navío actual de la búsqueda
                query = query.exclude(pk=self.instance.pk)
            
            if query.exists():
                self.add_error('imoNumero', 'Ya existe un navío con este número IMO.')

    def clean_imoNumero(self):
        imo = self.cleaned_data['imoNumero']
        if imo < 1000000 or imo > 9999999:
            raise forms.ValidationError("El número IMO debe tener exactamente 7 dígitos.")
        return imo

    def clean_capacidad(self):
        capacidad = self.cleaned_data['capacidad']
        if capacidad <= 0:
            raise forms.ValidationError("La capacidad debe ser mayor a cero.")
        return capacidad

    def clean_eslora(self):
        eslora = self.cleaned_data['eslora']
        if not (1 <= eslora <= 500):
            raise forms.ValidationError("La eslora debe estar entre 1 y 500 metros.")
        return eslora

    def clean_manga(self):
        manga = self.cleaned_data['manga']
        if not (1 <= manga <= 80):
            raise forms.ValidationError("La manga debe estar entre 1 y 80 metros.")
        return manga
    
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)

        # Mensajes personalizados en español para campos decimal
        self.fields['eslora'].error_messages['max_digits'] = 'La eslora no puede tener más de 8 cifras enteras.'
        self.fields['capacidad'].error_messages['max_digits'] = 'La capacidad no puede tener más de 8 cifras enteras.'
        self.fields['manga'].error_messages['max_digits'] = 'La manga no puede tener más de 8 cifras enteras.'
