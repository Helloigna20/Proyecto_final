# blog/admin.py

from django.contrib import admin
from .models import Pelicula, Comentario, Calificacion, Categoria # Importa todos tus modelos

# Personalización del Admin para Pelicula
@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'director', 'fecha_lanzamiento', 'puntuacion_media', 'fecha_creacion') # Campos que se muestran en la lista
    list_filter = ('fecha_lanzamiento', 'director') # Filtros laterales
    search_fields = ('titulo', 'director', 'actores') # Campos por los que se puede buscar
    prepopulated_fields = {'titulo': ('titulo',)} # Opcional: auto-rellena un campo (ej. slug) basado en otro
    fieldsets = ( # Organiza los campos en secciones en la página de edición
        (None, {
            'fields': ('titulo', 'categorias', 'sinopsis', 'portada', 'trailer_url', 'plataforma_url')
        }),
        ('Detalles de la Película', {
            'fields': ('director', 'actores', 'fecha_lanzamiento', 'puntuacion_media'),
            'classes': ('collapse',) # Hace que esta sección sea colapsable
        }),
    )

# Personalización del Admin para Comentario
@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('pelicula', 'autor', 'fecha_creacion', 'aprobado')
    list_filter = ('aprobado', 'fecha_creacion', 'pelicula')
    search_fields = ('autor__username', 'texto', 'pelicula__titulo') # Búsqueda por campos relacionados
    actions = ['aprobar_comentarios', 'desaprobar_comentarios'] # Acciones personalizadas en lista

    # Método para la acción personalizada "aprobar comentarios"
    @admin.action(description='Marcar comentarios seleccionados como aprobados')
    def aprobar_comentarios(self, request, queryset):
        updated = queryset.update(aprobado=True)
        self.message_user(request, f'{updated} comentarios marcados como aprobados.')

    # Método para la acción personalizada "desaprobar comentarios"
    @admin.action(description='Marcar comentarios seleccionados como desaprobados')
    def desaprobar_comentarios(self, request, queryset):
        updated = queryset.update(aprobado=False)
        self.message_user(request, f'{updated} comentarios marcados como desaprobados.')


# Personalización del Admin para Calificacion (Si lo creaste)
@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('pelicula', 'usuario', 'puntuacion', 'fecha_creacion')
    list_filter = ('puntuacion', 'fecha_creacion', 'pelicula')
    search_fields = ('usuario__username', 'pelicula__titulo')
    # readonly_fields = ('fecha_creacion',) # Puedes hacer campos de solo lectura

# Registra el nuevo modelo Categoria
admin.site.register(Categoria)

