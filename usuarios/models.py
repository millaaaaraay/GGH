from django.db import models

class Rol(models.Model):
    id_rol = models.AutoField(primary_key=True)
    nombre_rol = models.CharField(max_length=50)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Roles'

    def __str__(self):
        return self.nombre_rol

class Area(models.Model):
    id_area = models.AutoField(primary_key=True)
    nombre_area = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Areas'

    def __str__(self):
        return self.nombre_area

class Cargo(models.Model):
    id_cargo = models.AutoField(primary_key=True)
    nombre_cargo = models.CharField(max_length=100)
    descripcion = models.CharField(max_length=255, blank=True, null=True)

    class Meta:
        db_table = 'Cargos'

    def __str__(self):
        return self.nombre_cargo

class Usuario(models.Model):
    id_usuario = models.AutoField(primary_key=True)
    nombre = models.CharField(max_length=100)
    apellido = models.CharField(max_length=100)
    correo = models.EmailField(unique=True)
    contraseña = models.CharField(max_length=255)
    direccion = models.CharField(max_length=255, blank=True, null=True)
    telefono = models.CharField(max_length=50, blank=True, null=True)
    id_area = models.ForeignKey(Area, on_delete=models.SET_NULL, null=True, db_column='id_area')
    id_cargo = models.ForeignKey(Cargo, on_delete=models.SET_NULL, null=True, db_column='id_cargo')
    id_rol = models.ForeignKey(Rol, on_delete=models.PROTECT, db_column='id_rol')

    class Meta:
        db_table = 'Usuarios'

    def __str__(self):
        return f"{self.nombre} {self.apellido}"

class UsuarioAd(models.Model):
    usuario = models.OneToOneField(Usuario, on_delete=models.CASCADE, related_name='datos_ad')
    usuario_ad = models.CharField(max_length=50, blank=True, null=True)
    usuario_office = models.CharField(max_length=50, blank=True, null=True)
    usuario_sap = models.CharField(max_length=50, blank=True, null=True)
    equipo = models.CharField(max_length=100, blank=True, null=True)
    impresora = models.CharField(max_length=100, blank=True, null=True)
    movil = models.CharField(max_length=50, blank=True, null=True)

    class Meta:
        db_table = 'Usuarios_Ad'

    def __str__(self):
        return f"Datos AD de {self.usuario.nombre} {self.usuario.apellido}"

class RedSocial(models.Model):
    nombre = models.CharField(max_length=50)
    url = models.URLField()

    def __str__(self):
        return self.nombre


