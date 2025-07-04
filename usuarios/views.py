from django.shortcuts import render, redirect
from django.contrib import messages
from .forms import LoginForm
from .models import Usuario
from django.contrib.auth import logout as auth_logout
from django.http import HttpResponse

def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contraseña = form.cleaned_data['contraseña']
            try:
                usuario = Usuario.objects.get(correo=correo, contraseña=contraseña)
                request.session['usuario_id'] = usuario.id_usuario
                request.session['rol'] = usuario.id_rol.nombre_rol
                if usuario.id_rol.nombre_rol.lower() == 'administrador':
                    return redirect('panel_admin')
                else:
                    return redirect('panel_usuario')
            except Usuario.DoesNotExist:
                messages.error(request, 'Credenciales incorrectas')
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    return redirect('login')

def panel_admin(request):
    if request.session.get('rol') != 'Administrador':
        return HttpResponse('No autorizado', status=403)
    return HttpResponse('Bienvenido Administrador')

def panel_usuario(request):
    if request.session.get('rol') != 'Usuario':
        return HttpResponse('No autorizado', status=403)
    # Redirigir a la vista que muestra plantilla usuario.html
    return redirect('usuario')

def usuario_view(request):
    usuario_id = request.session.get('usuario_id', None)
    rol = request.session.get('rol', None)
    if not usuario_id or not rol:
        return redirect('login')
    context = {
        'usuario_id': usuario_id,
        'rol': rol,
    }
    return render(request, 'usuarios/usuario.html', context)
