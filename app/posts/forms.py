# mi_nuevo_blog/blog/forms.py

from django import forms
from django.contrib.auth.models import User # Necesitamos importar el modelo User para el formulario de registro
from .models import Comentario, Calificacion # Importa el modelo Comentario

class RegistroForm(forms.ModelForm):
    # Campos adicionales para el registro de usuario
    password = forms.CharField(label='Contraseña', widget=forms.PasswordInput)
    password2 = forms.CharField(label='Confirmar contraseña', widget=forms.PasswordInput)

    class Meta:
        model = User
        fields = ['username', 'email', 'password'] # Define los campos del modelo User que se usarán en el formulario
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
        }
        widgets = {
            'username': forms.TextInput(attrs={'class': 'form-control'}),
            'email': forms.EmailInput(attrs={'class': 'form-control'}),
            # El password ya lo manejamos con PasswordInput arriba, no aquí
        }

    # Validación adicional para asegurar que las contraseñas coinciden
    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password'] and cd['password2'] and cd['password'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd['password2']

    # Método para guardar el nuevo usuario
    def save(self, commit=True):
        user = super().save(commit=False) # Crea el objeto User pero no lo guarda aún
        user.set_password(self.cleaned_data['password']) # Establece la contraseña de forma segura
        if commit:
            user.save() # Guarda el usuario en la base de datos
        return user

class ComentarioForm(forms.ModelForm):
    class Meta:
        model = Comentario
        fields = ['texto'] # Solo queremos que el usuario edite el texto del comentario
        widgets = {
            'texto': forms.Textarea(attrs={
                'rows': 4, # Número de filas visible
                'placeholder': 'Escribe tu comentario aquí...',
                'class': 'form-control' # Puedes añadir clases CSS para estilizado
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