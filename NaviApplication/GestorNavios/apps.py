from django.apps import AppConfig

class GestornaviosConfig(AppConfig):
    default_auto_field = 'django.db.models.BigAutoField'
    name = 'GestorNavios'

    def ready(self):
       import GestorNavios.signals