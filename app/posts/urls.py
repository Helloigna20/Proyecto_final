
from django.urls import path
from . import views

urlpatterns = [
    path('', views.home, name='home'),


    path('pelicula/<int:pk>/', views.post, name='post'),

    path('accounts/login_register/', views.login_register, name='login_register'),

    path('accounts/logout/', views.cerrar_sesion, name='cerrar_sesion'),

     path('about/', views.about, name='about'),

     path('categoria/<slug:categoria_slug>/', views.peliculas_por_categoria, name='peliculas_por_categoria'),
]