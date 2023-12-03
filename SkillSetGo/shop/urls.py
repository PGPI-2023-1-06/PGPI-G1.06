from django.urls import path
from django.conf.urls import include
from . import views

app_name = 'shop'

urlpatterns = [
    path('search/', views.index, name='index'),
    path('', views.product_list, name='product_list'),
    path('cart/', views.cart, name='cart'), 
    path('checkout/', views.checkout, name='checkout'), 
    path('process_payment/', views.process_payment, name='process_payment'),
    path('update_item/', views.updateItem, name='update_item'),
    path('aboutUs/', views.aboutUs, name='aboutUs'),
    path('<slug:category_slug>/', views.product_list,name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,name='product_detail'),
    path('<int:id>/<slug:slug>/comment/', views.product_comment, name='product_comment'),
    path('payment/', include('payment.urls', namespace='payment')),
    path('update_item/', views.updateItem, name='update_item'),
    

]