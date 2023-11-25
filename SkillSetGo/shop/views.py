import json
from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Professor, Subject
from django.http import JsonResponse

# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    cartItems = order.get_cart_items
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = products.filter(category=category)
        
    return render(request,
    'shop/product/list.html',
    {'category': category,
    'categories': categories,
    'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
    id=id,
    slug=slug,
    available=True)

    return render(request,
    'shop/product/detail.html',
    {'product': product})

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, complete=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'shop/cart.html', context)

def updateItem(response):
    data = json.loads(response.data)
    productId = data['productId']
    action = data['action']

    customer = response.user
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, complete=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'remove':
        orderItem.delete()

    
    return JsonResponse('Item was added', safe=False)
