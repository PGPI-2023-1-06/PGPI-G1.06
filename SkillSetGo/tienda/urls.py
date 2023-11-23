from django.urls import path

from . import views

app_name = 'tienda'

urlpatterns = [
    path('', views.tienda, name='tienda'),
    path('carrito/', views.carrito, name='carrito'),
    path('checkout/', views.checkout, name='checkout'),
    
    #Urls respecto a las clases
    path('clase/listar/', views.listar_clases, name='listar_clases'),
    path('clase/<int:id>/', views.detalle_clase, name='detalle_clase'),
    path('clase/crear/', views.crear_clase, name='crear_clase'),
    path('clase/editar/<int:id>/', views.editar_clase, name='editar_clase'),
    path('clase/eliminar/<int:id>/', views.eliminar_clase, name='eliminar_clase')

]