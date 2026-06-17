from django.db import models
from django.contrib.auth.models import User
from django.db.models.signals import post_save
from django.dispatch import receiver
from GestorRecursos.models import Recurso,GestorRecursos
from datetime import datetime

class GestorNavios(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE)
    nombre = models.CharField(max_length=100)
    codigo_identificacion = models.CharField(max_length=50, unique=True)

    def __str__(self):
        return f"{self.nombre} - {self.codigo_identificacion}"


class Navio(models.Model):
    imoNumero = models.PositiveIntegerField(unique=True)
    nombre = models.CharField(max_length=100)
    capacidad = models.DecimalField(max_digits=10, decimal_places=2)
    eslora = models.DecimalField(max_digits=8, decimal_places=2)  # Longitud creo
    manga = models.DecimalField(max_digits=8, decimal_places=2)  # Anchura creo


    # Estados preefinidos
    estado = models.CharField(max_length=50, choices=[
        ('completo', 'Asignación completa'),
        ('inactivo', 'Inactivo'),
    ], default='inactivo')  

    def __str__(self):
        return f"{self.nombre} ({self.imoNumero}) - {self.estado}"
    
    def get_estado_color(self):
        return {
            'INACTIVO': 'bg-light-opacity',
            'COMPLETO': 'bg-success-opacity',
        }.get(self.estado.upper(), 'bg-white')



class Puerto (models.Model):
    nombre = models.CharField(max_length=100)
    ubicacion = models.CharField(max_length=100,default='Sin ubicacion', blank=True)

    def __str__(self):
        return self.nombre


# la escala esta formada por un navio y muchos puertos 
class Escala (models.Model):
    nombre = models.CharField(max_length=100)
    navio = models.ForeignKey(Navio, on_delete=models.CASCADE)
    puerto = models.ManyToManyField(Puerto, through="EscalaPuerto")

    def __str__(self):
        return f"{self.nombre} - {self.navio.nombre}"
    
    class Meta:
        verbose_name_plural = "Escalas"


#tuve que crear una clase intermedia porque no se puede hacer una relacion de muchos a muchos entre dos modelos digamos escala 1 puerto 1 , escala 1 puerto 2, escala 2 puerto 1, etc
class EscalaPuerto(models.Model):
    escala = models.ForeignKey(Escala, on_delete=models.CASCADE)
    puerto = models.ForeignKey(Puerto, on_delete=models.CASCADE)
    fecha_arribo = models.DateTimeField(default=datetime(2000, 1, 1, 0, 0))
    fecha_zarpe = models.DateTimeField(default=datetime(2000, 1, 1, 0, 0))

    def __str__(self):
        return f"{self.escala.navio.nombre} en {self.puerto.nombre}"
    
    class Meta:
        verbose_name_plural = "Escalas y Puertos"



#Estas son las filas digamos de lo presupuesto y asi cada que asignes un nuevo recursos solo crea una nueva instancia de esta clase
#Digamos queres asignar 1 kit de herramientas y una grua al puerto X de la escala Y
#tons solo crea una instancia de esta clase una para la herramienta definis la cantidad y otra para la grua y asi
class AsignacionRecursos(models.Model):
    escala_puerto = models.ForeignKey(EscalaPuerto, on_delete=models.CASCADE,default=None, null=True)
    recurso = models.ForeignKey(Recurso, on_delete=models.CASCADE)
    cantidad = models.PositiveIntegerField(default=1)
    fecha_asignacion = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.recurso.nombre} - {self.cantidad} unidades asignadas a {self.escala_puerto.puerto.nombre} ({self.escala_puerto.escala.navio.nombre})"