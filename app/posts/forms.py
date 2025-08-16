from django import forms
from django.contrib.auth.models import User 
from .models import Comentario, Calificacion

class RegistroForm(forms.ModelForm):
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
        fields = ['username', 'email']
        labels = {
            'username': 'Nombre de Usuario',
            'email': 'Correo Electrónico',
        }
        widgets = {
            'email': forms.EmailInput(attrs={'class': 'form-control', 'placeholder': 'Correo electrónico'}),
            'username': forms.TextInput(attrs={'class': 'form-control', 'placeholder': 'Nombre de usuario'}),
        }

    def clean_password2(self):
        cd = self.cleaned_data
        if cd['password1'] and cd['password2'] and cd['password1'] != cd['password2']:
            raise forms.ValidationError('Las contraseñas no coinciden.')
        return cd['password2']


    def save(self, commit=True):
        user = super().save(commit=False)
        user.set_password(self.cleaned_data['password1']) 
        if commit:
            user.save()
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