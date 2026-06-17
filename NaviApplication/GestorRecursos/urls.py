from django.urls import path
from . import views

urlpatterns = [
    #path('login_recurso/', views.login_recurso, name='login_recurso'),
    path('registro/', views.registro, name='registro'),
    path('dashboard/', views.dashboard, name='dashboard'),
    path('crear-recurso/', views.registrar_recurso, name='registrar_recurso'),
    path('logout/', views.logout_GestorRecursos, name='logout_GestorRecursos'),
    path('gestores-json/', views.lista_gestores_recursos_json, name='gestores_json'),
    path('gestores-separados-json/', views.lista_gestores_recursos_separados_json, name='gestores_separados_json'),
    path('perfil/', views.editar_perfil, name='editar_perfil'),
    path('recurso/eliminar/<int:recurso_id>/', views.eliminar_recurso, name='eliminar_recurso'),
    path('recurso/detalles/<int:recurso_id>/', views.detalles_recurso, name='detalles_recurso'),
    path('recursos/recurso/editar/<int:recurso_id>/', views.editar_recurso, name='editar_recurso'),

]