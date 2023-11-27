from django.urls import path
from . import views

app_name = 'shop'

urlpatterns = [
    path('search/', views.index, name='index'),
    path('', views.product_list, name='product_list'),
    path('cart/', views.cart, name='cart'), 
    path('checkout/', views.checkout, name='checkout'), 
    path('<slug:category_slug>/', views.product_list,name='product_list_by_category'),
    path('<int:id>/<slug:slug>/', views.product_detail,name='product_detail'),
    path('<int:id>/<slug:slug>/comment/', views.product_comment, name='product_comment'),
    path('update_item/', views.updateItem, name='update_item'),
    

]