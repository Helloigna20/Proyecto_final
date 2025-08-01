# blog/urls.py

from django.urls import path
from . import views # Importa tus vistas

urlpatterns = [
    # URL para la lista de todas las películas
    path('', views.home, name='home'),

    # URL para el detalle de una película específica (usando su ID)
    # CAMBIO AQUÍ: 'pelicula_id' se cambió a 'pk' para coincidir con la vista
    path('pelicula/<int:pk>/', views.post, name='post'),

    # URL para la pantalla de inicio de sesión/registro
    path('accounts/login_register/', views.login_register, name='login_register'),

    # URL para cerrar sesión
    path('accounts/logout/', views.cerrar_sesion, name='cerrar_sesion'),
]