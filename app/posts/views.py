# blog/views.py

from django.shortcuts import render, redirect, get_object_or_404
from django.contrib.auth.forms import AuthenticationForm # Solo AuthenticationForm, no UserCreationForm de Django
from django.contrib.auth import login, logout, authenticate
from django.contrib import messages
from django.contrib.auth.decorators import login_required
from .models import Pelicula, Comentario, Calificacion, Categoria # Asegúrate de que Calificacion también esté importada si la usas
from .forms import ComentarioForm, RegistroForm # Importa tu RegistroForm personalizado desde .forms



# Vista para la página principal que muestra todas las películas
def listado_peliculas(request):
    peliculas = Pelicula.objects.all()
    return render(request, 'listado_peliculas.html', {'peliculas': peliculas})


# Vista que filtra las películas por categoría
def peliculas_por_categoria(request, categoria_slug):
    # Obtener el objeto de la categoría o mostrar un 404 si no existe
    categoria = get_object_or_404(Categoria, slug=categoria_slug)
    
    # Filtrar las películas que pertenecen a la categoría
    peliculas = Pelicula.objects.filter(categorias=categoria)
    
    # Preparar el contexto para la plantilla
    context = {
        'categoria_actual': categoria,
        'peliculas': peliculas,
    }
    
    return render(request, 'home.html', context)


# --- Vista para la lista de películas ---
def home(request):
    peliculas = Pelicula.objects.all().order_by('-fecha_lanzamiento')

    # Lógica para manejar el envío de comentarios desde la lista de películas
    if request.method == 'POST':
        if 'submit_comment' in request.POST:
            if not request.user.is_authenticated:
                messages.error(request, 'Debes iniciar sesión para comentar.')
                return redirect('login_register')

            pelicula_id = request.POST.get('pelicula_id')
            pelicula_para_comentar = get_object_or_404(Pelicula, id=pelicula_id)

            # Usamos el prefijo para diferenciar los formularios en el POST
            # No es necesario re-instanciar con request.POST aquí si el formulario ya ha sido validado en la lista
            # El prefijo ya está en el request.POST['comentario_X-texto']
            form_comentario_enviado = ComentarioForm(request.POST, prefix=f'comentario_{pelicula_id}')

            if form_comentario_enviado.is_valid():
                comentario = form_comentario_enviado.save(commit=False)
                comentario.autor = request.user
                comentario.pelicula = pelicula_para_comentar
                comentario.save()
                messages.success(request, "Tu comentario ha sido añadido con éxito. Podría requerir aprobación.")
                return redirect('home') # Redirige para evitar reenvío de formulario
            else:
                messages.error(request, "Error al añadir el comentario. Por favor, revisa el formulario.")
                # Si hay un error, el usuario será redirigido y el mensaje de error se mostrará.
                # No se intentará recargar el formulario con errores específicos para esta vista compleja.

    # Prepara los datos para la plantilla, incluyendo formularios de comentarios para cada película
    peliculas_con_datos_adicionales = []
    for pelicula in peliculas:
        recent_comments = pelicula.comentarios.filter(aprobado=True).order_by('-fecha_creacion')[:3]
        form_para_esta_pelicula = None
        if request.user.is_authenticated:
            # Creamos una nueva instancia de ComentarioForm para cada película
            # con un prefijo único para manejar múltiples formularios en la misma página.
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

# --- Vista para el detalle de una película específica ---
def post(request, pk): # Usamos 'pk' como argumento para que coincida con la URL estándar
    pelicula = get_object_or_404(Pelicula, pk=pk) # Usa 'pk' aquí también

    # Lógica para manejar el envío de comentarios desde la página de detalle
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
        # Crea el formulario vacío para GET o si el POST falló y necesitamos mostrar errores
        if form_comentario is None: # Si no se instanció ya con errores
            form_comentario = ComentarioForm()
    else:
        # Mensaje informativo si el usuario no está autenticado
        messages.info(request, "Inicia sesión para dejar un comentario.")
        form_comentario = None # Asegurarse de que no se pase un formulario si no está logueado

    # Obtener todos los comentarios APROBADOS para esta película
    comentarios = pelicula.comentarios.filter(aprobado=True).order_by('-fecha_creacion') # Ordena los más nuevos primero

    context = {
        'pelicula': pelicula,
        'comentarios': comentarios,
        'form_comentario': form_comentario,
    }
    return render(request, 'post.html', context)


# --- Vista de inicio de sesión y registro ---
def login_register(request):
    login_form = AuthenticationForm()
    register_form = RegistroForm() # Usa tu RegistroForm personalizado aquí

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

        elif 'register_submit' in request.POST: # Botón de registro presionado
            register_form = RegistroForm(request.POST) # Usa tu RegistroForm aquí
            if register_form.is_valid():
                user = register_form.save()
                login(request, user) # Inicia sesión al usuario automáticamente después del registro
                messages.success(request, "¡Cuenta creada exitosamente! Has iniciado sesión.")
                return redirect('home')
            else:
                # Si el formulario de registro no es válido, los errores estarán en register_form
                messages.error(request, "Error al registrarse. Por favor, corrige los errores.")

    context = {
        'login_form': login_form,
        'register_form': register_form,
    }
    return render(request, 'login_register.html', context)

# --- Vista para cerrar sesión ---
@login_required
def cerrar_sesion(request):
    logout(request)
    messages.info(request, "Has cerrado tu sesión.")
    return redirect('home') # Redirige a la home por defecto

#nosotros
def about(request):
    """
    Vista para renderizar la página "Nosotros" o "Contacto".
    """
    return render(request, 'about.html')