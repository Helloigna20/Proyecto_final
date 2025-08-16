from django.contrib import admin
from .models import Pelicula, Comentario, Calificacion, Categoria 

# Personalización del Admin para Pelicula
@admin.register(Pelicula)
class PeliculaAdmin(admin.ModelAdmin):
    list_display = ('titulo', 'director', 'fecha_lanzamiento', 'puntuacion_media', 'fecha_creacion')
    list_filter = ('fecha_lanzamiento', 'director')
    search_fields = ('titulo', 'director', 'actores')
    prepopulated_fields = {'titulo': ('titulo',)}
    fieldsets = ( 
        (None, {

            'fields': ('titulo', 'categorias', 'sinopsis', 'portada', 'trailer_url', 'plataforma_url')
        }),
        ('Detalles de la Película', {
            'fields': ('director', 'actores', 'fecha_lanzamiento', 'puntuacion_media'),
            'classes': ('collapse',) # Hace que esta sección sea colapsable
        }),
    )

@admin.register(Comentario)
class ComentarioAdmin(admin.ModelAdmin):
    list_display = ('pelicula', 'autor', 'fecha_creacion', 'aprobado')
    list_filter = ('aprobado', 'fecha_creacion', 'pelicula')
    search_fields = ('autor__username', 'texto', 'pelicula__titulo')
    actions = ['aprobar_comentarios', 'desaprobar_comentarios']

    @admin.action(description='Marcar comentarios seleccionados como aprobados')
    def aprobar_comentarios(self, request, queryset):
        updated = queryset.update(aprobado=True)
        self.message_user(request, f'{updated} comentarios marcados como aprobados.')

    @admin.action(description='Marcar comentarios seleccionados como desaprobados')
    def desaprobar_comentarios(self, request, queryset):
        updated = queryset.update(aprobado=False)
        self.message_user(request, f'{updated} comentarios marcados como desaprobados.')


@admin.register(Calificacion)
class CalificacionAdmin(admin.ModelAdmin):
    list_display = ('pelicula', 'usuario', 'puntuacion', 'fecha_creacion')
    list_filter = ('puntuacion', 'fecha_creacion', 'pelicula')
    search_fields = ('usuario__username', 'pelicula__titulo')

admin.site.register(Categoria)

