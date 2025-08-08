# mi_nuevo_blog/blog/forms.py

from django import forms
from django.contrib.auth.models import User # Necesitamos importar el modelo User para el formulario de registro
from .models import Comentario, Calificacion # Importa el modelo Comentario

class RegistroForm(forms.ModelForm):
    # Campos adicionales para el registro de usuario
    password1 = forms.CharField(
        label='Contraseña', 
        widget=forms.PasswordInput(attrs={'placeholder': 'Contraseña'})
    )
    password2 = forms.CharField(
        label='Confirmar contraseña', 
        widget=forms.PasswordInput(attrs={'placeholder': 'Repetir Contraseña'})
    )

    class Meta:
        model = User
        fields = ['username', 'email'] # Define los campos del modelo User que se usarán en el formulario
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
            # El password ya lo manejamos con PasswordInput arriba, no aquí
        }

    # Validación adicional para asegurar que las contraseñas coinciden
    def clean_password2(self):
        cd = self.cleaned_data
        # --- Cambio aquí ---
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd['password2']

    # Método para guardar el nuevo usuario
    def save(self, commit=True):
        user = super().save(commit=False) # Crea el objeto User pero no lo guarda aún
        # --- Cambio aquí ---
        user.set_password(self.cleaned_data['password1']) # Establece la contraseña de forma segura
        if commit:
            user.save() # Guarda el usuario en la base de datos
        return user

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto']
        widgets = {
            'texto': forms.Textarea(attrs={
                'class': 'form-control',
                'placeholder': 'Escribe tu comentario aquí...',
                'maxlength': '500',
                'rows': 2,
            }),
        }
        labels = {
            'texto': 'Tu Comentario',
        }

# Si tuvieras un formulario para Calificacion, también iría aquí
class CalificacionForm(forms.ModelForm):
     class Meta:
         model = Calificacion
         fields = ['puntuacion']
         widgets = {
             'puntuacion': forms.Select(choices=[(i, str(i)) for i in range(1, 6)], attrs={'class': 'form-control'}),
         }
         labels = {
             'puntuacion': 'Tu Calificación',
         }