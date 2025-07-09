from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('administrador/', views.panel_admin, name='panel_admin'),
    path('usuario/', views.panel_usuario, name='panel_usuario'),
    path('usuario-perfil/', views.usuario_view, name='usuario'),
    path('gestion-usuarios/', views.gestion_usuarios_view, name='gestion_usuarios'),
    
    # Agrega esta ruta para Usuarios AD
    path('usuarios-ad/', views.usuarios_ad_view, name='usuarios_ad'),
    path('ventas/', views.ventas_view, name='ventas'),
]
