from django.db import models
from django.contrib.auth.models import User

class GestorRecursos(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    telefono = models.CharField(max_length=15,default='Sin telefono', blank=True) 
    direccion = models.CharField(max_length=255,default='Sin direccion', blank=True)   
    descripcion = models.TextField(blank=True, default='Sin descripcion',max_length=500)
    correo = models.EmailField(max_length=254,unique=True, default='Sin correo', blank=True)

    def __str__(self):
        return f"{self.user.username} - {self.telefono}"
    
class Recurso(models.Model):
    nombre = models.CharField(max_length=100)
    precio = models.DecimalField(max_digits=10, decimal_places=2, default=0.00)
    descripcion = models.TextField(blank=True, default='Sin descripcion', max_length=500)
    imagen = models.ImageField(upload_to='recursos/', blank=True, null=True)    
    tipo = models.CharField(max_length=50)
    subtipo = models.CharField(max_length=50, blank=True, null=True)
    gestor = models.ForeignKey(GestorRecursos, on_delete=models.CASCADE)
    puertos_disponibles = models.ManyToManyField("GestorNavios.Puerto", blank=True, related_name="recursos_disponibles")

    def recursos_imagen_upload__path(instance, filename):
        return f'recursos/{instance.gestor.user.username}/{filename}'

    def __str__(self):
        return f"{self.nombre} - {self.gestor.user.username}"
    
    class Meta:
        verbose_name_plural = "Recursos"


