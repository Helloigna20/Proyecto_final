# blog/models.py

from django.db import models
from django.contrib.auth.models import User # Necesitamos importar User para el autor de los comentarios y calificaciones
from django.db.models import Avg # Importamos Avg para calcular promedios

class Pelicula(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    descripcion = models.TextField(verbose_name="Descripción")
    fecha_lanzamiento = models.DateField(verbose_name="Fecha de Lanzamiento")
    director = models.CharField(max_length=100, verbose_name="Director")
    actores = models.TextField(verbose_name="Actores Principales", help_text="Separar actores por comas")
    portada = models.ImageField(upload_to='peliculas/portadas/', null=True, blank=True, verbose_name="Portada de la Película")
    # Agregamos campos para la URL del trailer o la puntuación general
    trailer_url = models.URLField(max_length=200, null=True, blank=True, verbose_name="URL del Trailer (YouTube/Vimeo)")
    puntuacion_media = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, verbose_name="Puntuación Media")
    # Puedes añadir un campo para el género, lo haremos con un ManyToManyField si creamos el modelo Categoria

    # Campos de timestamp para saber cuándo fue creada/actualizada la entrada de la película
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")

    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Película"
        verbose_name_plural = "Películas"
        ordering = ['-fecha_lanzamiento', 'titulo'] # Ordena por fecha de lanzamiento descendente, luego por título


class Comentario(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='comentarios', verbose_name="Película")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios_escritos', verbose_name="Autor del Comentario")
    texto = models.TextField(verbose_name="Comentario")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Publicación")
    aprobado = models.BooleanField(default=True, verbose_name="Aprobado") # Para moderación

    def __str__(self):
        return f'Comentario de {self.autor.username} en {self.pelicula.titulo}'

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ['-fecha_creacion'] # Ordena los comentarios más nuevos primero


# Opcional: Para calificar películas
class Calificacion(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='calificaciones', verbose_name="Película")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calificaciones_realizadas', verbose_name="Usuario")
    puntuacion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Puntuación (1-5)") # Ej: 1 a 5 estrellas
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Calificación")

    class Meta:
        unique_together = ('pelicula', 'usuario') # Un usuario solo puede calificar una película una vez
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.usuario.username} calificó {self.pelicula.titulo} con {self.puntuacion}'

    # Puedes agregar lógica aquí para actualizar la puntuación media de la película
    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)
        # Actualizar la puntuación media de la película cuando se guarda una calificación
        # Usamos .aggregate(Avg('puntuacion')) para calcular el promedio. 'or 0.0' es para manejar si no hay calificaciones.
        self.pelicula.puntuacion_media = self.pelicula.calificaciones.aggregate(Avg('puntuacion'))['puntuacion__avg'] or 0.0
        self.pelicula.save()

    def delete(self, *args, **kwargs):
        pelicula_id = self.pelicula.id # Guarda el ID antes de borrar
        super().delete(*args, **kwargs)
        # Recalcular la puntuación media de la película cuando se borra una calificación
        # Es importante obtener la película de nuevo, ya que 'self.pelicula' podría ser nulo después del super().delete()
        pelicula = Pelicula.objects.get(id=pelicula_id)
        pelicula.puntuacion_media = pelicula.calificaciones.aggregate(Avg('puntuacion'))['puntuacion__avg'] or 0.0
        pelicula.save()