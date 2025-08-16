# app/posts/templatetags/blog_filters.py

from django import template

register = template.Library()

@register.filter
def replace_youtube_url(url):
    """
    Convierte una URL de YouTube estándar (watch?v=) en una URL de embed (embed/).
    Esto es necesario para que el video se pueda incrustar correctamente en un iframe.
    """
    if url:
        return url.replace("watch?v=", "embed/")
    return ""