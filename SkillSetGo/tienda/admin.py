from django.contrib import admin
from .models import *

# Register your models here.

@admin.register(Clase)
class PostAdmin(admin.ModelAdmin):
    list_display = ['nombre', 'precio',]
    list_filter = ['nombre', 'precio',]
    search_fields = ['nombre', 'precio', 'descripcion',]

    ordering = ['nombre', 'precio', ]


admin.site.register(Cliente)
admin.site.register(Pedido)
admin.site.register(ClaseEnPedido)

