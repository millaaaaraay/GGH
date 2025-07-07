from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('administrador/', views.panel_admin, name='panel_admin'),
    path('usuario/', views.panel_usuario, name='panel_usuario'),
    path('usuario-perfil/', views.usuario_view, name='usuario'),
    path('gestion-usuarios/', views.gestion_usuarios_view, name='gestion_usuarios'),
    path('usuarios/agregar/', views.agregar_usuario_view, name='agregar_usuario'),
    path('usuarios/editar/<int:id_usuario>/', views.editar_usuario_view, name='editar_usuario'),

    # Aquí agregamos la ruta para usuarios_ad
    path('usuarios/ad/', views.usuarios_ad_view, name='usuarios_ad'),
]
