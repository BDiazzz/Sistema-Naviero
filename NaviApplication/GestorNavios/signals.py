
from django.db.models.signals import post_save
from django.dispatch import receiver
from django.contrib.auth.models import User
from .models import GestorNavios

# Señal para crear un GestorNavios cuando se crea un superusuario !NO TOCAR 
@receiver(post_save, sender=User)
def crear_gestor_navios(sender, instance, created, **kwargs):
    if created and instance.is_superuser:
        GestorNavios.objects.create(user=instance, nombre=instance.username, codigo_identificacion=f"ADM-{instance.id}")
