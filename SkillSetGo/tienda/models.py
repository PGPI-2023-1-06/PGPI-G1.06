from django.db import models
from django.contrib.auth.models import User

# Create your models here.

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    nombre = models.CharField(max_length=200, null=True)
    correo = models.CharField(max_length=200, null=True)

    def __str__(self):
        return self.nombre

class Clase(models.Model):
    nombre = models.CharField(max_length=200, null=True)
    precio = models.FloatField()
    descripcion = models.TextField()
    # imagen

    class Meta:
        ordering = ['nombre']
        # index para mejorar tiempo de execucion de consultas con el campo "nombre"
        indexes = [
            models.Index(fields=['nombre']),
        ]

    def __str__(self):
        return self.nombre


class Pedido(models.Model):
    cliente = models.ForeignKey(Cliente, on_delete=models.SET_NULL, null=True, blank=True, related_name='pedidos')
    fecha_pedido = models.DateTimeField(auto_now_add=True)
    completado = models.BooleanField(default=False) # para saber si todavia es posible añadir productos al pedido
    pedidoID = models.CharField(max_length=200, null=True)

    def __str__(self):
        return str(self.id)

# un producto en un pedido
class ClaseEnPedido(models.Model):
    producto = models.ForeignKey(Clase, on_delete=models.SET_NULL, blank=True, null=True)
    pedido = models.ForeignKey(Pedido, on_delete=models.SET_NULL, blank=True, null=True)
    cantidad = models.IntegerField(default=0, null=True, blank=True)
    fecha_anadido = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.producto.nombre)