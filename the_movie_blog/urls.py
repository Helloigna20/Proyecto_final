#the_movie_blog/urls.py

"""
URL configuration for core project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.2/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""
from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static

urlpatterns = [
    path('admin/', admin.site.urls),
    path('', include('app.posts.urls')),  # Incluye las URLs de la aplicación blog
    # Si tienes otras aplicaciones, puedes incluir sus URLs a
    # path('account/', include('django.contrib.auth.urls')),  # URLs de autenticación
]

if settings.DEBUG:
    # Esto sirve los archivos de medios (subidas de usuarios)
    urlpatterns += static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
    # ¡Esta es la línea que falta para los archivos estáticos!
    urlpatterns += static(settings.STATIC_URL, document_root=settings.STATIC_ROOT)
