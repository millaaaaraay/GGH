from django import forms
from .models import Usuario, UsuarioAd
from .models import Empresas, TipoSolicitud, OrigenCotizacion, NProveedor, RutProveedor, UDM



class LoginForm(forms.Form):
    correo = forms.EmailField(label='Correo')
    contraseña = forms.CharField(label='Contraseña', widget=forms.PasswordInput)

class UsuarioForm(forms.ModelForm):
    class Meta:
        model = Usuario
        fields = ['nombre', 'apellido', 'correo', 'contraseña', 'direccion', 'telefono', 'id_area', 'id_cargo', 'id_rol']

class UsuarioAdForm(forms.ModelForm):
    class Meta:
        model = UsuarioAd
        fields = ['usuario', 'usuario_ad', 'usuario_office', 'usuario_sap', 'equipo', 'impresora', 'movil']

class CreacionCodigoForm(forms.Form):
    fecha = forms.DateField(
        label="Fecha",
        widget=forms.DateInput(attrs={'type': 'date', 'class': 'form-control'})
    )
    nombre = forms.CharField(
        label="Nombre Solicitante",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    empresa = forms.ModelChoiceField(
        queryset=Empresas.objects.all(),
        label="Empresa",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    tipo_solicitud = forms.ModelChoiceField(
        queryset=TipoSolicitud.objects.all(),
        label="Tipo Solicitud",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    cotizacion = forms.CharField(
        required=False,
        label="Cotización",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    origen = forms.ModelChoiceField(
        queryset=OrigenCotizacion.objects.all(),
        label="Origen Cotización",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    n_proveedor = forms.ModelChoiceField(
        queryset=NProveedor.objects.all(),
        label="Nombre Proveedor",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    rut = forms.ModelChoiceField(
        queryset=RutProveedor.objects.all(),
        label="RUT Proveedor",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    sku_fab_modelo = forms.CharField(
        required=False,
        label="SKU FAB/MODELO",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    sku_proveedor = forms.CharField(
        required=False,
        label="SKU Proveedor",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    marca = forms.CharField(
        required=False,
        label="Marca",
        widget=forms.TextInput(attrs={'class': 'form-control'})
    )
    udm = forms.ModelChoiceField(
        queryset=UDM.objects.all(),
        label="UDM",
        widget=forms.Select(attrs={'class': 'form-control'})
    )
    largo = forms.DecimalField(
        required=False,
        label="Largo",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el largo'})
    )
    ancho = forms.DecimalField(
        required=False,
        label="Ancho",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el ancho'})
    )
    alto = forms.DecimalField(
        required=False,
        label="Alto",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el alto'})
    )
    peso = forms.DecimalField(
        required=False,
        label="Peso",
        widget=forms.NumberInput(attrs={'class': 'form-control', 'placeholder': 'Ingrese el peso'})
    )
    costo = forms.DecimalField(
        required=False,
        label="Costo",
        widget=forms.NumberInput(attrs={'class': 'form-control'})
    )
    descripcion = forms.CharField(
        required=False,
        label="Descripción",
        widget=forms.Textarea(attrs={'class': 'form-control', 'rows': 2})
    )
