from . import views
from django.urls import path

urlpatterns = [
    #path("login/", views.login_navios, name="login_navios"),
    path("GestionarNavios/", views.gestionar_navios, name="gestionar_navios"),
    path("crearEditarNavio/", views.crear_editar_navio, name="crear_editar_navio"),
    path("crearEditarNavio/<int:navio_id>/", views.crear_editar_navio, name="editar_navio"),
    path("eliminarNavio/<int:navio_id>/", views.eliminar_navio, name="eliminar_navio"),
    path('logout/', views.cerrar_sesion, name='cerrar_sesion'), 
    path("GestionarRecursos/<int:escala_id>/", views.gestionar_recursos, name="gestionar_recursos"),
    path("EscalasSinRecursos/", views.escalas_sin_recursos, name="escalas_sin_recursos"),
    path("EscalasSinRecursos/<int:navio_id>/", views.escalas_sin_recursos, name="escalas_sin_recursos_navio"),
    path('confirmar_asignacion/<int:escala_id>/', views.confirmar_asignacion, name='confirmar_asignacion'),
    path("gestionar_escala/<int:navio_id>/", views.gestionar_escala, name="gestionar_escala"),  # Usa guion bajo
    path('presupuesto/<int:escala_id>/', views.generar_presupuesto_pdf, name='generar_presupuesto_pdf'),
    path('get_escalas_con_recursos/<int:navio_id>/', views.get_escalas_con_recursos, name='get_escalas_con_recursos'),
    path('escala/editar/<int:escala_id>/', views.editar_escala, name='editar_escala'),
    path('escala/eliminar/<int:escala_id>/', views.eliminar_escala, name='eliminar_escala'),
    path('navios/escalasConRecursos/', views.escalas_con_recursos, name='escalas_con_recursos'),
    path('navios/escalasConRecursos/<int:navio_id>/', views.escalas_con_recursos, name='escalas_con_recursos_filtrado'),
]
