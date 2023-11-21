from django.db import models
from django.contrib.auth.models import User
import re

from django.forms import ValidationError

class Cliente(models.Model):
    usuario = models.OneToOneField(User, on_delete=models.CASCADE, null=False, blank=False, default='')
    nombre = models.CharField(max_length=200, null=True, unique=True)
    apellidos = models.CharField(max_length=200, null=True)
    correo = models.EmailField(max_length=200, null=True, unique=True)
    cuentaRedSocial = models.CharField(max_length=200, null=True)
    direccion = models.CharField(max_length=200, null=True)
    numero_telefono = models.CharField(max_length=200, null=True)
    
    def __str__(self):
        return self.nombre

    def clean(self):
        super().clean()
        if self.numero_telefono:
            # check phone number format
            if not re.match(r'^\d{9}$', self.numero_telefono):
                raise ValidationError('El número de teléfono no tiene un formato válido. Debe tener 9 dígitos.')
                    
class Clase(models.Model):
    
    nombre = models.CharField(max_length=200, null=False, blank=False, default='') 
    descripcion = models.TextField()
    nivel = models.CharField(max_length=200, null=True)
    instructor = models.CharField(max_length=200, null=True)
    requisitos = models.TextField(null=True)
    precio = models.FloatField()
    horario = models.CharField(max_length=200, null=True)
    duracion = models.IntegerField(default=0, null=False, blank=True)
    ubicacion = models.CharField(max_length=200, null=True)
    cuposMaximo = models.IntegerField(default=0, null=False, blank=True)
    cuposActual = models.IntegerField(default=0, null=False, blank=True)
    imagen = models.ImageField(null=True, blank=True)

    class Meta:
        ordering = ['nombre']
        # index para mejorar tiempo de execucion de consultas con el campo "nombre"
        indexes = [
            models.Index(fields=['nombre']),
        ]

    def __str__(self):
        return self.nombre
    
    @property
    def get_total_carrito(self):
        items = self.itemspedido_set.all()
        total = sum([item.get_total for item in items])
        return total
    
    @property
    def get_pedidos_carrito(self):
        items = self.itemspedido_set.all()
        pedidos = sum([item.cantidad for item in items])
        return pedidos
    

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