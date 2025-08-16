from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Pelicula, Comentario, Calificacion, Categoria
from .forms import ComentarioForm, RegistroForm



def listado_peliculas(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'listado_peliculas.html', {'peliculas': peliculas})


def peliculas_por_categoria(request, categoria_slug):
    categoria = get_object_or_404(Categoria, slug=categoria_slug)
    
    peliculas = Pelicula.objects.filter(categorias=categoria)
    
    context = {
        'categoria_actual': categoria,
        'peliculas': peliculas,
    }
    
    return render(request, 'home.html', context)


def home(request):
    peliculas = Pelicula.objects.all().order_by('-fecha_lanzamiento')

    if request.method == 'POST':
        if 'submit_comment' in request.POST:
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para comentar.')
                return redirect('login_register')

            pelicula_id = request.POST.get('pelicula_id')
            pelicula_para_comentar = get_object_or_404(Pelicula, id=pelicula_id)


            form_comentario_enviado = ComentarioForm(request.POST, prefix=f'comentario_{pelicula_id}')

            if form_comentario_enviado.is_valid():
                comentario = form_comentario_enviado.save(commit=False)
                comentario.autor = request.user
                comentario.pelicula = pelicula_para_comentar
                comentario.save()
                messages.success(request, "Tu comentario ha sido añadido con éxito. Podría requerir aprobación.")
                return redirect('home')
            else:
                messages.error(request, "Error al añadir el comentario. Por favor, revisa el formulario.")

    peliculas_con_datos_adicionales = []
    for pelicula in peliculas:
        recent_comments = pelicula.comentarios.filter(aprobado=True).order_by('-fecha_creacion')[:3]
        form_para_esta_pelicula = None
        if request.user.is_authenticated:

            form_para_esta_pelicula = ComentarioForm(prefix=f'comentario_{pelicula.id}')

        peliculas_con_datos_adicionales.append({
            'pelicula': pelicula,
            'recent_comments': recent_comments,
            'form_comentario_instance': form_para_esta_pelicula,
        })

    context = {
        'peliculas_con_datos_adicionales': peliculas_con_datos_adicionales,
    }
    return render(request, 'home.html', context)

def post(request, pk):
    pelicula = get_object_or_404(Pelicula, pk=pk)

    form_comentario = None
    if request.user.is_authenticated:
        if request.method == 'POST':
            if 'submit_comment' in request.POST:
                form_comentario = ComentarioForm(request.POST)
                if form_comentario.is_valid():
                    comentario = form_comentario.save(commit=False)
                    comentario.autor = request.user
                    comentario.pelicula = pelicula
                    comentario.save()
                    messages.success(request, "Tu comentario ha sido enviado para revisión.")
                    return redirect('post', pk=pelicula.pk) # Redirige con 'pk'
                else:
                    messages.error(request, "Error al enviar el comentario. Por favor, revisa.")
        if form_comentario is None: # Si no se instanció ya con errores
            form_comentario = ComentarioForm()
    else:
        messages.info(request, "Inicia sesión para dejar un comentario.")
        form_comentario = None

    comentarios = pelicula.comentarios.filter(aprobado=True).order_by('-fecha_creacion') # Ordena los más nuevos primero

    context = {
        'pelicula': pelicula,
        'comentarios': comentarios,
        'form_comentario': form_comentario,
    }
    return render(request, 'post.html', context)


def login_register(request):
    login_form = AuthenticationForm()
    register_form = RegistroForm()

    if request.method == 'POST':
        if 'login_submit' in request.POST: # Botón de login presionado
            login_form = AuthenticationForm(request, data=request.POST)
            if login_form.is_valid():
                username = login_form.cleaned_data.get('username')
                password = login_form.cleaned_data.get('password')
                user = authenticate(request, username=username, password=password)
                if user is not None:
                    login(request, user)
                    messages.success(request, f"¡Bienvenido de nuevo, {username}!")
                    return redirect('home')
                else:
                    messages.error(request, "Usuario o contraseña incorrectos.")
            else:
                messages.error(request, "Por favor, corrige los errores en el formulario de inicio de sesión.")

        elif 'register_submit' in request.POST: 
            register_form = RegistroForm(request.POST)
            if register_form.is_valid():
                user = register_form.save()
                login(request, user)
                messages.success(request, "¡Cuenta creada exitosamente! Has iniciado sesión.")
                return redirect('home')
            else:
                messages.error(request, "Error al registrarse. Por favor, corrige los errores.")

    context = {
        'login_form': login_form,
        'register_form': register_form,
    }
    return render(request, 'login_register.html', context)

@login_required
def cerrar_sesion(request):
    logout(request)
    messages.info(request, "Has cerrado tu sesión.")
    return redirect('home')

#nosotros
def about(request):
    """
    Vista para renderizar la página "Nosotros" o "Contacto".
    """
    return render(request, 'about.html')