from django import forms
from .models import Usuario, UsuarioAd

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
