from django.db import models
from django.contrib.auth.models import User
from django.db.models import Avg
from django.utils.text import slugify


class Categoria(models.Model):
    nombre = models.CharField(max_length=100, unique=True)
    slug = models.SlugField(max_length=100, unique=True, blank=True)

    def save(self, *args, **kwargs):
        if not self.slug:
            self.slug = slugify(self.nombre)
        super().save(*args, **kwargs)

    def __str__(self):
        return self.nombre

    class Meta:
        verbose_name_plural = "Categorías"


class Pelicula(models.Model):
    titulo = models.CharField(max_length=200, verbose_name="Título")
    sinopsis = models.TextField(verbose_name="Sinopsis", help_text="Breve descripción de la película", blank=True, null=True)
    fecha_lanzamiento = models.DateField(verbose_name="Fecha de Lanzamiento")
    director = models.CharField(max_length=100, verbose_name="Director")
    actores = models.TextField(verbose_name="Actores Principales", help_text="Separar actores por comas")
    portada = models.ImageField(upload_to='peliculas/portadas/', null=True, blank=True, verbose_name="Portada de la Película")
    trailer_url = models.URLField(max_length=200, null=True, blank=True, verbose_name="URL del Trailer (YouTube/Vimeo)")
    puntuacion_media = models.DecimalField(max_digits=3, decimal_places=1, default=0.0, verbose_name="Puntuación Media")
    categorias = models.ManyToManyField(Categoria, related_name='peliculas')
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Creación")
    fecha_actualizacion = models.DateTimeField(auto_now=True, verbose_name="Última Actualización")
    plataforma_url = models.URLField(
        blank=True, 
        null=True, 
        verbose_name="Enlace a Plataforma"
    )
    def __str__(self):
        return self.titulo

    class Meta:
        verbose_name = "Película"
        verbose_name_plural = "Películas"
        ordering = ['-fecha_lanzamiento', 'titulo']


class Comentario(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='comentarios', verbose_name="Película")
    autor = models.ForeignKey(User, on_delete=models.CASCADE, related_name='comentarios_escritos', verbose_name="Autor del Comentario")
    texto = models.TextField(verbose_name="Comentario")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Publicación")
    aprobado = models.BooleanField(default=True, verbose_name="Aprobado")

    def __str__(self):
        return f'Comentario de {self.autor.username} en {self.pelicula.titulo}'

    class Meta:
        verbose_name = "Comentario"
        verbose_name_plural = "Comentarios"
        ordering = ['-fecha_creacion']


class Calificacion(models.Model):
    pelicula = models.ForeignKey(Pelicula, on_delete=models.CASCADE, related_name='calificaciones', verbose_name="Película")
    usuario = models.ForeignKey(User, on_delete=models.CASCADE, related_name='calificaciones_realizadas', verbose_name="Usuario")
    puntuacion = models.IntegerField(choices=[(i, str(i)) for i in range(1, 6)], verbose_name="Puntuación (1-5)")
    fecha_creacion = models.DateTimeField(auto_now_add=True, verbose_name="Fecha de Calificación")

    class Meta:
        unique_together = ('pelicula', 'usuario')
        verbose_name = "Calificación"
        verbose_name_plural = "Calificaciones"
        ordering = ['-fecha_creacion']

    def __str__(self):
        return f'{self.usuario.username} calificó {self.pelicula.titulo} con {self.puntuacion}'

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        self.pelicula.puntuacion_media = self.pelicula.calificaciones.aggregate(Avg('puntuacion'))['puntuacion__avg'] or 0.0
        self.pelicula.save()

    def delete(self, *args, **kwargs):
        pelicula_id = self.pelicula.id
        super().delete(*args, **kwargs)
        pelicula = Pelicula.objects.get(id=pelicula_id)
        pelicula.puntuacion_media = pelicula.calificaciones.aggregate(Avg('puntuacion'))['puntuacion__avg'] or 0.0
        pelicula.save()