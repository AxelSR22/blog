from django.contrib.auth.decorators import user_passes_test

def superuser_required(view_func):
    def _wrapped_view(request, *args, **kwargs):
        if request.user.is_superuser:
            return view_func(request, *args, **kwargs)
        else:
            return redirect('home')  # Redirige a la página de inicio si el usuario no es un superusuario.
    return _wrapped_view
