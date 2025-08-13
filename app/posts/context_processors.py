from .models import Categoria

def categorias_disponibles(request):
    return {
        'categorias_menu': Categoria.objects.all()
    }