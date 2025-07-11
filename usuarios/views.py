from django.shortcuts import render, redirect, get_object_or_404
from django.contrib import messages
from django.http import HttpResponse
from django.contrib.auth import logout as auth_logout
from .forms import LoginForm, UsuarioForm
from .models import (
    Usuario, UsuarioAd, RedSocial, Area, Cargo, Rol,
    Empresas, TipoSolicitud, OrigenCotizacion, Origen, NProveedor,
    RutProveedor, UDM
)
from django.db.models import Q
from django.core.mail import EmailMessage
from django.conf import settings
from django.urls import reverse
import json
from django.utils.safestring import mark_safe


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

def panel_usuario(request):
    usuario_id = request.session.get('usuario_id')
    rol = request.session.get('rol', '').lower()
    if rol != 'usuario' or not usuario_id:
        return HttpResponse('No autorizado', status=403)
    usuario = None
    try:
        usuario = Usuario.objects.get(id_usuario=usuario_id)
    except Usuario.DoesNotExist:
        usuario = None
    ventas_url = reverse('ventas')
    context = {
        'usuario': usuario,
        'rol': rol,
        'ventas_url': ventas_url,
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
        'nombre_buscar': nombre_buscar,
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

# ----------------------------------------
# ESTA ES LA VIEW DEL FORMULARIO DE CÓDIGOS
# ----------------------------------------
def creacion_codigo_view(request):
    # Une proveedores con rut usando el id
    nproveedores = list(NProveedor.objects.all().order_by('id_nproveedor'))
    rutproveedores = {rp.id_rut: rp.rut_proveedor for rp in RutProveedor.objects.all()}

    proveedores_combo = []
    for np in nproveedores:
        proveedores_combo.append({
            'id': np.id_nproveedor,
            'nombre': np.nombre_nproveedor,
            'rut': rutproveedores.get(np.id_nproveedor, '')
        })
    proveedores_combo_limited = proveedores_combo[:5]  # SOLO LOS 5 PRIMEROS

    if request.method == 'POST':
        fecha = request.POST.get('fecha')
        vendedor_id = request.POST.get('nombre')
        empresa_id = request.POST.get('id_empresa')
        tipo_solicitud_id = request.POST.get('tipo_solicitud')
        origen_cotizacion_id = request.POST.get('origen')
        origen_producto_id = request.POST.get('origen_producto')
        n_proveedor_id = request.POST.get('n_proveedor')
        sku_proveedor = request.POST.get('sku_proveedor')
        sku_fab_modelo = request.POST.get('sku_fab_modelo')
        descriptor = request.POST.get('descriptor')
        marca = request.POST.get('marca')
        udm_id = request.POST.get('udm')
        largo_valor = request.POST.get('largo_valor')
        largo_unidad = request.POST.get('largo_unidad')
        ancho_valor = request.POST.get('ancho_valor')
        ancho_unidad = request.POST.get('ancho_unidad')
        alto_valor = request.POST.get('alto_valor')
        alto_unidad = request.POST.get('alto_unidad')
        peso_valor = request.POST.get('peso_valor')
        peso_unidad = request.POST.get('peso_unidad')

        archivos = request.FILES.getlist('archivos_cotizacion')

        # Obtención de nombres para email
        try:
            vendedor = Usuario.objects.get(id_usuario=vendedor_id)
            nombre_vendedor = f"{vendedor.nombre} {vendedor.apellido}"
        except:
            nombre_vendedor = ""
        try:
            empresa = Empresas.objects.get(id_empresa=empresa_id).nombre_empresa
        except:
            empresa = empresa_id
        try:
            tipo_solicitud = TipoSolicitud.objects.get(id_tipo_solicitud=tipo_solicitud_id).nombre_tipo_solicitud
        except:
            tipo_solicitud = tipo_solicitud_id
        try:
            origen_cotizacion = OrigenCotizacion.objects.get(id_origen=origen_cotizacion_id).origen_cotizacion
        except:
            origen_cotizacion = origen_cotizacion_id
        try:
            origen_producto = Origen.objects.get(id_origen=origen_producto_id).nombre_origen
        except:
            origen_producto = origen_producto_id
        try:
            proveedor = NProveedor.objects.get(id_nproveedor=n_proveedor_id)
            rut_proveedor = RutProveedor.objects.get(id_rut=n_proveedor_id)
            nombre_proveedor = proveedor.nombre_nproveedor
            rut = rut_proveedor.rut_proveedor
        except:
            nombre_proveedor = ""
            rut = ""
        try:
            udm = UDM.objects.get(id_udm=udm_id).nombre_udm
        except:
            udm = udm_id

        # Validación de adjuntos obligatorios según tipo de cotización
        if (str(origen_cotizacion).strip().upper() in ['POR DOCUMENTO', 'WHATSAPP']) and not archivos:
            context = {
                'empresas': Empresas.objects.all(),
                'tipos_solicitud': TipoSolicitud.objects.all(),
                'origenes': OrigenCotizacion.objects.all(),
                'origenes_productos': Origen.objects.all(),
                'proveedores_combo': proveedores_combo_limited,
                'proveedores_combo_json': mark_safe(json.dumps(proveedores_combo_limited)),
                'udms': UDM.objects.all(),
                'areas_ventas': Area.objects.filter(nombre_area__icontains='VENTA'),
                'usuarios_vendedores': Usuario.objects.filter(id_cargo=3),
                'error_msg': 'Debe adjuntar al menos un archivo para este tipo de cotización.'
            }
            return render(request, 'usuarios/creacioncodigo.html', context)

        # Ejemplo de envío de correo
        subject = "Nueva Solicitud de Código"
        body = f"""
Fecha: {fecha}
Vendedor: {nombre_vendedor}
Empresa: {empresa}
Origen del Producto: {origen_producto}
Tipo de Solicitud: {tipo_solicitud}
Origen Cotización: {origen_cotizacion}
Proveedor: {nombre_proveedor}
Rut Proveedor: {rut}
SKU Proveedor: {sku_proveedor}
SKU Fabricante/Modelo: {sku_fab_modelo}
Descriptor: {descriptor}
Marca: {marca}
UDM: {udm}
Largo: {largo_valor} {largo_unidad}
Ancho: {ancho_valor} {ancho_unidad}
Alto: {alto_valor} {alto_unidad}
Peso: {peso_valor} {peso_unidad}
        """
        to_email = ['tucorreo@dominio.cl']
        email = EmailMessage(subject, body, settings.DEFAULT_FROM_EMAIL, to_email)
        for archivo in archivos[:4]:
            email.attach(archivo.name, archivo.read(), archivo.content_type)
        email.send()

        return render(request, 'usuarios/solicitud_enviada.html')

    # GET: carga normal
    context = {
        'empresas': Empresas.objects.all(),
        'tipos_solicitud': TipoSolicitud.objects.all(),
        'origenes': OrigenCotizacion.objects.all(),
        'origenes_productos': Origen.objects.all(),
        'proveedores_combo': proveedores_combo_limited,
        'proveedores_combo_json': mark_safe(json.dumps(proveedores_combo_limited)),
        'udms': UDM.objects.all(),
        'areas_ventas': Area.objects.filter(nombre_area__icontains='VENTA'),
        'usuarios_vendedores': Usuario.objects.filter(id_cargo=3),
    }
    return render(request, 'usuarios/creacioncodigo.html', context)