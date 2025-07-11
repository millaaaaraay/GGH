from django.db import models

# ---- ENTIDADES DE USUARIOS Y ESTRUCTURA ----

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

# ---- TABLAS DE NEGOCIO Y MAESTROS ----

class Empresas(models.Model):
    id_empresa = models.AutoField(primary_key=True)
    nombre_empresa = models.CharField(max_length=255)
    class Meta:
        db_table = 'Empresas'
    def __str__(self):
        return self.nombre_empresa

class Origen(models.Model):
    id_origen = models.AutoField(primary_key=True)
    nombre_origen = models.CharField(max_length=100)
    class Meta:
        db_table = 'origen'
    def __str__(self):
        return self.nombre_origen

class OrigenCotizacion(models.Model):
    id_origen = models.AutoField(primary_key=True)
    origen_cotizacion = models.CharField(max_length=255)
    class Meta:
        db_table = 'OrigenCotizacion'
    def __str__(self):
        return self.origen_cotizacion

class TipoSolicitud(models.Model):
    id_tipo_solicitud = models.AutoField(primary_key=True)
    nombre_tipo_solicitud = models.CharField(max_length=255)
    class Meta:
        db_table = 'TipoSolicitud'
    def __str__(self):
        return self.nombre_tipo_solicitud

class UDM(models.Model):
    id_udm = models.AutoField(primary_key=True)
    nombre_udm = models.CharField(max_length=50)
    class Meta:
        db_table = 'UDM'
    def __str__(self):
        return self.nombre_udm

# ---- PROVEEDORES ----

class NProveedor(models.Model):
    id_nproveedor = models.AutoField(primary_key=True)
    nombre_nproveedor = models.CharField(max_length=255)
    class Meta:
        db_table = 'NProveedor'
    def __str__(self):
        return self.nombre_nproveedor

class RutProveedor(models.Model):
    id_rut = models.AutoField(primary_key=True)
    rut_proveedor = models.CharField(max_length=20)
    class Meta:
        db_table = 'RutProveedor'
    def __str__(self):
        return self.rut_proveedor

# ---- OTROS CATÁLOGOS ----

class Conversion(models.Model):
    id_conversion = models.AutoField(primary_key=True)
    nombre_conversion = models.CharField(max_length=50)
    class Meta:
        db_table = 'Conversion'
    def __str__(self):
        return self.nombre_conversion

class SinSKU(models.Model):
    id_sinsku = models.AutoField(primary_key=True)
    nombre_sinsku = models.CharField(max_length=50)
    class Meta:
        db_table = 'SinSKU'
    def __str__(self):
        return self.nombre_sinsku

class ConvKilos(models.Model):
    id_convkilos = models.AutoField(primary_key=True)
    nombre_convkilos = models.CharField(max_length=50)
    class Meta:
        db_table = 'ConvKilos'
    def __str__(self):
        return self.nombre_convkilos

class DescripcionCatalogo(models.Model):
    id_descripcion = models.AutoField(primary_key=True)
    nombre_descripcion = models.CharField(max_length=255)
    class Meta:
        db_table = 'DescripcionCatalogo'
    def __str__(self):
        return self.nombre_descripcion

# ---- SOLICITUDES ----

class SolicitudCodigos(models.Model):
    id = models.AutoField(primary_key=True)
    fecha = models.DateField()
    nombre = models.CharField(max_length=255)
    id_empresa = models.ForeignKey(Empresas, on_delete=models.CASCADE, db_column='id_empresa')
    tipo_solicitud = models.ForeignKey(TipoSolicitud, on_delete=models.CASCADE, db_column='tipo_solicitud')
    cotizacion = models.CharField(max_length=100, blank=True, null=True)
    origen = models.ForeignKey(OrigenCotizacion, on_delete=models.SET_NULL, null=True, db_column='origen')
    n_proveedor = models.CharField(max_length=100, blank=True, null=True)
    rut = models.ForeignKey(RutProveedor, on_delete=models.CASCADE, db_column='rut')
    sku_proveedor = models.CharField(max_length=100, blank=True, null=True)
    sku_fab_modelo = models.CharField(max_length=100, blank=True, null=True)
    descriptor = models.CharField(max_length=100, blank=True, null=True)
    marca = models.CharField(max_length=100, blank=True, null=True)
    udm = models.ForeignKey(UDM, on_delete=models.CASCADE, db_column='udm')
    largo = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    ancho = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    alto = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    class Meta:
        db_table = 'SolicitudCodigos'
    def __str__(self):
        return self.nombre
