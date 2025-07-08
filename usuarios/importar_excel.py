import os
import django
import pandas as pd

os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'gghweb.settings')
django.setup()

from usuarios.models import Area, Rol, Usuario, UsuarioAd

def importar_usuarios_ad(ruta_excel):
    df = pd.read_excel(ruta_excel, engine='openpyxl', header=3)  # Cabecera en fila 4 (index 3)

    for _, fila in df.iterrows():
        area_nombre = fila.get('ÁREA', '').strip() if pd.notna(fila.get('ÁREA', '')) else ''
        nombre_completo = fila.get('NOMBRE', '').strip() if pd.notna(fila.get('NOMBRE', '')) else ''

        if not area_nombre or not nombre_completo:
            print("Fila saltada por área o nombre vacío")
            continue

        if nombre_completo.upper() in ['DISPONIBLE', 'DISPONIBLE2']:
            print(f"Usuario especial ignorado: {nombre_completo}")
            continue

        area, _ = Area.objects.get_or_create(nombre_area=area_nombre)

        rol = Rol.objects.get(id_rol=1) if area_nombre.upper() == 'SISTEMAS' else Rol.objects.get(id_rol=2)

        partes_nombre = nombre_completo.split()
        nombre = partes_nombre[0]
        apellido = " ".join(partes_nombre[1:]) if len(partes_nombre) > 1 else ''

        correo_excel = fila.get('USUARIO OFFICE', '').strip() if pd.notna(fila.get('USUARIO OFFICE', '')) else ''
        correo = correo_excel.lower() if correo_excel else f"{nombre.lower()}.{apellido.lower()}@ggh.cl"

        if Usuario.objects.filter(correo=correo).exists():
            print(f"Correo duplicado, usuario no creado: {correo}")
            continue

        usuario = Usuario.objects.create(
            nombre=nombre,
            apellido=apellido,
            correo=correo,
            contraseña='default123',
            id_area=area,
            id_rol=rol,
        )

        UsuarioAd.objects.create(
            usuario=usuario,
            usuario_ad=fila.get('USUARIO AD', '').strip() if pd.notna(fila.get('USUARIO AD', '')) else '',
            usuario_office=correo_excel,
            usuario_sap=fila.get('USUARIOS SAP', '').strip() if pd.notna(fila.get('USUARIOS SAP', '')) else '',
            equipo=fila.get('Equipo', '').strip() if pd.notna(fila.get('Equipo', '')) else '',
            impresora=fila.get('Impresora', '').strip() if pd.notna(fila.get('Impresora', '')) else '',
            movil=fila.get('Movil', '').strip() if pd.notna(fila.get('Movil', '')) else '',
        )

        print(f"Usuario creado: {usuario}")

if __name__ == '__main__':
    ruta = r"C:\Users\millaray\Documents\Usuarios AD revisado.xlsx"
    importar_usuarios_ad(ruta)
