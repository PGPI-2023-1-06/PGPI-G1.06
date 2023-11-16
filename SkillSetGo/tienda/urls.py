from django.urls import path

from . import views

app_name = 'tienda'

urlpatterns = [
    path('', views.tienda, name='tienda'),
    path('catalogo/', views.catalogo, name='catalogo'),
    path('catalogo/<int:id>/', views.clase_detalle, name='clase_detalle'),
    path('carrito/', views.carrito, name='carrito'),
    path('pedido/', views.pedido, name='pedido'),

]