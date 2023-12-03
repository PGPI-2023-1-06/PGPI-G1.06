from django.urls import path
from . import views
app_name = 'payment'
urlpatterns = [
    path('completed/<int:order_id>/', views.payment_completed, name='completed'),
    path('process/<int:order_id>/', views.payment_process, name='process'),
    path('canceled/', views.payment_canceled, name='canceled'),
]