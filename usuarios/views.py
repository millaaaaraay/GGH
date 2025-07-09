from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from .forms import LoginForm, UsuarioForm
from .models import Usuario, RedSocial
from .models import Usuario, Area, Cargo, Rol
from django.db.models import Q


# views.py (inicio)

from .models import Usuario, UsuarioAd, RedSocial


def login_view(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            correo = form.cleaned_data['correo']
            contraseña = form.cleaned_data['contraseña']
            try:
                usuario = Usuario.objects.get(correo=correo, contraseña=contraseña)
                request.session['usuario_id'] = usuario.id_usuario
                request.session['rol'] = usuario.id_rol.nombre_rol.lower()

                if request.session['rol'] == 'administrador':
                    return redirect('panel_admin')
                elif request.session['rol'] == 'usuario':
                    return redirect('panel_usuario')
                else:
                    messages.error(request, 'Rol no reconocido')
                    return render(request, 'usuarios/login.html', {'form': form})
            except Usuario.DoesNotExist:
                messages.error(request, 'Credenciales incorrectas')
                return render(request, 'usuarios/login.html', {'form': form})
    else:
        form = LoginForm()
    return render(request, 'usuarios/login.html', {'form': form})

def logout_view(request):
    auth_logout(request)
    request.session.flush()
    return redirect('login')

def panel_admin(request):
    rol = request.session.get('rol', '').lower()
    if rol != 'administrador':
        return HttpResponse('No autorizado', status=403)
    
    usuario = None
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        try:
            usuario = Usuario.objects.get(id_usuario=usuario_id)
        except Usuario.DoesNotExist:
            usuario = None
    
    context = {
        'rol': rol,
        'usuario': usuario,
    }
    return render(request, 'usuarios/administrador.html', context)

from django.shortcuts import render
from django.http import HttpResponse
from .models import Usuario

from django.urls import reverse

def panel_usuario(request):
    usuario_id = request.session.get('usuario_id')
    rol = request.session.get('rol', '').lower()

    # Validar rol y sesión
    if rol != 'usuario' or not usuario_id:
        return HttpResponse('No autorizado', status=403)

    usuario = None
    try:
        usuario = Usuario.objects.get(id_usuario=usuario_id)
    except Usuario.DoesNotExist:
        print(f"DEBUG: Usuario con id {usuario_id} no encontrado")
        usuario = None

    # Agregar la url de ventas al contexto
    ventas_url = reverse('ventas')

    context = {
        'usuario': usuario,
        'rol': rol,
        'ventas_url': ventas_url,   # <--- aquí lo agregas
    }
    return render(request, 'usuarios/usuario.html', context)





def usuario_view(request):
    usuario_id = request.session.get('usuario_id')
    rol = request.session.get('rol')
    if not usuario_id or not rol:
        return redirect('login')
    context = {
        'usuario_id': usuario_id,
        'rol': rol,
    }
    return render(request, 'usuarios/usuario.html', context)

def redes_sociales(request):
    return {
        'redes': RedSocial.objects.all()
    }



def gestion_usuarios_view(request):
    rol = request.session.get('rol', '').lower()
    if rol != 'administrador':
        return HttpResponse('No autorizado', status=403)
    
    usuario_actual = None
    usuario_id = request.session.get('usuario_id')
    if usuario_id:
        try:
            usuario_actual = Usuario.objects.get(id_usuario=usuario_id)
        except Usuario.DoesNotExist:
            usuario_actual = None

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            messages.success(request, 'Usuario creado correctamente.')
            return redirect('gestion_usuarios')
        else:
            messages.error(request, 'Por favor, corrige los errores en el formulario.')
    else:
        form = UsuarioForm()

    # Obtener valor del parámetro GET para búsqueda
    nombre_buscar = request.GET.get('nombre', '').strip()

    usuarios = Usuario.objects.all()
    if nombre_buscar:
        usuarios = usuarios.filter(
            Q(nombre__icontains=nombre_buscar) | Q(apellido__icontains=nombre_buscar)
        )

    areas = Area.objects.all()
    cargos = Cargo.objects.all()
    roles = Rol.objects.all()

    context = {
        'rol': rol,
        'usuario': usuario_actual,
        'usuarios': usuarios,
        'form': form,
        'areas': areas,
        'cargos': cargos,
        'roles': roles,
        'nombre_buscar': nombre_buscar,  # para mantener valor en formulario
    }
    return render(request, 'usuarios/gestion_usuarios.html', context)





def editar_usuario_view(request, id_usuario):
    rol = request.session.get('rol', '').lower()
    if rol != 'administrador':
        return HttpResponse('No autorizado', status=403)
    
    usuario = get_object_or_404(Usuario, id_usuario=id_usuario)
    
    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('gestion_usuarios')
    else:
        form = UsuarioForm(instance=usuario)
    
    return render(request, 'usuarios/editar_usuario.html', {'form': form, 'usuario': usuario})



from django.shortcuts import render, get_object_or_404, redirect
from django.http import HttpResponse
from .forms import UsuarioForm
from .models import Usuario

def agregar_usuario_ad_view(request):
    rol = request.session.get('rol', '').lower()
    if rol != 'administrador':
        return HttpResponse('No autorizado', status=403)

    if request.method == 'POST':
        form = UsuarioForm(request.POST)
        if form.is_valid():
            form.save()
            return redirect('usuarios_ad')
    else:
        form = UsuarioForm()

    return render(request, 'agregar_usuario_ad.html', {'form': form})


def editar_usuario_ad_view(request, id_usuario_ad):
    rol = request.session.get('rol', '').lower()
    if rol != 'administrador':
        return HttpResponse('No autorizado', status=403)

    usuario = get_object_or_404(Usuario, id_usuario=id_usuario_ad)

    if request.method == 'POST':
        form = UsuarioForm(request.POST, instance=usuario)
        if form.is_valid():
            form.save()
            return redirect('usuarios_ad')
    else:
        form = UsuarioForm(instance=usuario)

    return render(request, 'editar_usuario_ad.html', {'form': form, 'usuario': usuario})


def usuarios_ad_view(request):
    usuarios = Usuario.objects.select_related('datos_ad', 'id_area').all()
    return render(request, 'usuarios/usuarios_ad.html', {'usuarios': usuarios})


def ventas_view(request):
    return render(request, 'usuarios/ventas.html')