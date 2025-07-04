from django.urls import path
from . import views

urlpatterns = [
    path('login/', views.login_view, name='login'),
    path('logout/', views.logout_view, name='logout'),
    path('panel_admin/', views.panel_admin, name='panel_admin'),
    path('panel_usuario/', views.panel_usuario, name='panel_usuario'),
    path('usuario/', views.usuario_view, name='usuario'),

    
]
