from django.shortcuts import render, redirect, get_object_or_404
from .models import Posts, Categoria, Comment
from .forms import PostForm, ContactoForm, CommentForm
from django.core.mail import send_mail
from django.conf import settings
from django.contrib.auth.decorators import login_required
from django.contrib.auth import authenticate, login
from django.contrib.auth.forms import UserCreationForm
from django.contrib import messages
from django.contrib.auth.decorators import user_passes_test
from .decorators import superuser_required



def home(request):
    posts = Posts.objects.all()
    context = {'posts': posts}
    return render(request, 'Posts/posts_page.html', context)

def formulario(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para agregar una publicación.')
        return redirect('login')

    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Publicación creada exitosamente!')
            return redirect('home')

    context = {'form': form}
    return render(request, 'Posts/form_post.html', context)

@superuser_required
def deletePost(request, pk):
    post = Posts.objects.get(id=pk)
    if request.method == 'POST':
        post.delete()
        return redirect('home')

    context = {'post': post}
    return render(request, 'delete_template.html', context)

@superuser_required
def updatePost(request, pk):
    post = Posts.objects.get(id=pk)
    form = PostForm(instance=post)
    update = 1

    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES, instance=post)
        if form.is_valid():
            form.save()
            messages.success(request, '¡Publicación actualizada exitosamente!')
            return redirect('home')

    context = {"form": form, "update": update}
    return render(request, 'Posts/form_post.html', context)


def categorias(request):
    categorias = Categoria.objects.all()
    context = {'categorias': categorias}
    return render(request, 'categorias.html', context)

def detalle_categoria(request, pk):
    categoria = Categoria.objects.get(id=pk)
    peliculas = Posts.objects.filter(categoria=categoria)
    context = {'categoria': categoria, 'peliculas': peliculas}
    return render(request, 'detalle_categoria.html', context)


def about(request):
    description = """
    ¡Bienvenidos a PELIS_BLOG! Mi nombre es Sabadini Axel creador de este blog, aqui podrán explorar un catálogo de películas organizadas por categorías,
    lo que les permitirá descubrir nuevos títulos y revivir clásicos favoritos.
    Quiero destacar que este blog fue creado como parte de mi aprendizaje en el curso de INFORMATORIO, donde me asignaron
    la emocionante tarea de desarrollar una página web dedicada al cine. A lo largo del curso, he adquirido valiosas
    habilidades en diseño web y desarrollo, lo que me ha permitido construir este espacio con dedicación y esfuerzo.

    En PELIS_BLOG, no solo encontrarán reseñas y análisis detallados de películas, sino que también tendrán la
    capacidad de interactuar con el contenido. Pueden agregar, actualizar y eliminar publicaciones, y dentro de
    cada artículo, tienen la oportunidad de dejar sus comentarios y compartir sus propias opiniones sobre las películas
    que tanto amamos.

    Espero que disfruten explorando este blog tanto como yo disfruté creándolo. ¡Gracias por ser parte de esta
    comunidad cinéfila y por compartir esta pasión conmigo!
    """
    context = {
        'description': description,
    }
    return render(request, 'about.html', context)

@login_required
def formulario(request):
    if not request.user.is_authenticated:
        messages.error(request, 'Debes iniciar sesión para agregar una publicación.')
        return redirect('login')

    form = PostForm()
    if request.method == 'POST':
        form = PostForm(request.POST, request.FILES)
        if form.is_valid():
            form.save()
            return redirect('home')

    context = {'form': form}
    return render(request, 'Posts/form_post.html', context)


def contacto(request):
    if request.method == 'POST':
        form = ContactoForm(request.POST)
        if form.is_valid():
            nombre = form.cleaned_data['nombre']
            apellido = form.cleaned_data['apellido']
            email = form.cleaned_data['email']
            consulta = form.cleaned_data['consulta']

            # Envío del correo electrónico
            subject = f'Consulta de {nombre} {apellido}'
            message = f'Nombre: {nombre}\nApellido: {apellido}\nEmail: {email}\nConsulta: {consulta}'
            send_mail(subject, message, settings.DEFAULT_FROM_EMAIL, ['axels.r92@gmail.com'])

            # Puedes agregar aquí un mensaje de éxito o redireccionar a una página de éxito
            return render(request, 'contacto_exito.html')

    else:
        form = ContactoForm()

    context = {'form': form}
    return render(request, 'contacto.html', context)

def login_view(request):
    if request.method == 'POST':
        username = request.POST['username']
        password = request.POST['password']
        user = authenticate(request, username=username, password=password)
        if user is not None:
            login(request, user)
            return redirect('home')
        else:
            return render(request, 'login.html', {'error': 'Usuario o contraseña incorrectos'})

    return render(request, 'login.html')

@login_required
def logout_view(request):
    logout(request)
    return redirect('home')

def profile(request):
    return render(request, 'profile.html')

def post(request, pk):
    post = Posts.objects.get(id=pk)
    categoria = post.categoria
    peliculas = Posts.objects.filter(categoria=categoria)

    # Obtener todos los comentarios para esta publicación
    comments = Comment.objects.filter(post=post)

    # Procesar el formulario de comentarios si es una solicitud POST
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.save()
            # Redirigir a la misma página después de enviar el comentario
            return redirect('post', pk=pk)
    else:
        form = CommentForm()

    context = {'post': post, 'peliculas': peliculas, 'comments': comments, 'form': form}
    return render(request, 'Posts/post.html', context)

def edit_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    if request.method == 'POST':
        form = CommentForm(request.POST, instance=comment)
        if form.is_valid():
            form.save()
            # Redirigir a la página de detalle de la publicación después de editar el comentario
            return redirect('post', pk=comment.post.id)
    else:
        form = CommentForm(instance=comment)

    context = {'form': form}
    return render(request, 'edit_comment.html', context)

@login_required
def delete_comment(request, comment_id):
    comment = get_object_or_404(Comment, id=comment_id)

    # Verificar si el usuario logueado es el autor del comentario
    if comment.author == request.user.username:
        comment.delete()

    return redirect('post', pk=comment.post.id)

def registro(request):
    if request.method == 'POST':
        form = UserCreationForm(request.POST)
        if form.is_valid():
            form.save()
            username = form.cleaned_data.get('username')
            messages.success(request, f'¡Usuario {username} registrado exitosamente! Por favor, inicia sesión.')
            # Redirigir al usuario a la página de inicio de sesión después del registro exitoso
            return redirect('login')
    else:
        form = UserCreationForm()

    context = {'form': form}
    return render(request, 'registro.html', context)

def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            # Redirige al usuario a la página de inicio (o a donde desees) si no es superusuario
            return redirect('home')

    return _wrapped_view


def post(request, pk):
    post = Posts.objects.get(id=pk)
    categoria = post.categoria
    peliculas = Posts.objects.filter(categoria=categoria)

    # Obtener todos los comentarios para esta publicación
    comments = Comment.objects.filter(post=post)

    # Procesar el formulario de comentarios si es una solicitud POST
    if request.method == 'POST':
        form = CommentForm(request.POST)
        if form.is_valid():
            comment = form.save(commit=False)
            comment.post = post
            comment.author = request.user.username  # Asignar el autor del comentario
            comment.save()
            # Redirigir a la misma página después de enviar el comentario
            return redirect('post', pk=pk)
    else:
        form = CommentForm()

    context = {'post': post, 'peliculas': peliculas, 'comments': comments, 'form': form}
    return render(request, 'Posts/post.html', context)