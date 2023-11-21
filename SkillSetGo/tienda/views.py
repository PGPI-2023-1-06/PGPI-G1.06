from django.shortcuts import redirect, render, get_object_or_404

from .forms import ClaseForm
from .models import *

def tienda(request):
    context = {}
    return render(request, 'tienda/tienda.html', context)


def carrito(request):
    if request.user.is_authenticated:
        cliente = request.user.cliente
        pedido, created = Pedido.objects.get_or_create(cliente=cliente, completado=False)
        items = pedido.itemspedido_set.all()
    else:
        items = []
        pedido = {'get_pedidos_carrito':0, 'get_total_carrito':0}

    context = {'items':items, 'pedido':pedido}
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


#Vistas respecto a  las clases

def listar_clases(request):
    clases = Clase.objects.all()
    return render(request, 'clase/lista.html', {'clases': clases})

def detalle_clase(request, id):
    clase = get_object_or_404(Clase, id=id)

    return render(request, 'clase/detalle.html', {'clase': clase})

def crear_clase(request):
    if request.method == "POST":
        form = ClaseForm(request.POST)
        if form.is_valid():
            clase = form.save()
            return redirect('detalle_clase', id=clase.id)
    else:
        form = ClaseForm()
    return render(request, 'clase/crear.html', {'form': form})

def editar_clase(request, id):
    clase = get_object_or_404(Clase, id=id)
    if request.method == "POST":
        form = ClaseForm(request.POST, instance=clase)
        if form.is_valid():
            clase = form.save()
            return redirect('detalle_clase', id=clase.id)
    else:
        form = ClaseForm(instance=clase)
    return render(request, 'clase/editar.html', {'form': form})

def eliminar_clase(request, id):
    clase = get_object_or_404(Clase, id=id)
    clase.delete()
    return redirect('listar_clases')