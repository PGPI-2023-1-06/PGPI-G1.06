from django.shortcuts import render, get_object_or_404
from .models import *

# Create your views here.


def tienda(request):
    context = {}
    return render(request, 'tienda/tienda.html', context)


def carrito(request):
    context = {}
    return render(request, 'tienda/carrito.html', context)

def pedido(request):
    context = {}
    return render(request, 'tienda/pedido.html', context)

def catalogo(request):
    clases = Clase.objects.all()
    return render(request, 'tienda/clase/catalogo.html', {'clases': clases})

def clase_detalle(request, id):
    clase = get_object_or_404(Clase, id=id)

    return render(request, 'tienda/clase/detalle.html', {'clase': clase})