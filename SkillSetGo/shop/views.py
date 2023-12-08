from django.utils import timezone
import json
from django.shortcuts import render, get_object_or_404
from django.db.models import Q  
from django.views.decorators.http import require_POST
from .forms import *
from .models import Category, Product, Professor, Subject, Customer, Order, OrderItem ,Comment
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib.auth.decorators import login_required
from django.contrib import messages
from .utils import *


# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = products.filter(category=category)
    
    # necessary for the shopping cart digit
    if not request.user.is_superuser:
        data = cartData(request)
        cartItems = data['cartItems']

        return render(request,
        'shop/product/list.html',
        {'category': category,
        'categories': categories,
        'products': products, 
        'cartItems': cartItems,})
    return render(request,
        'shop/product/list.html',
        {'category': category,
        'categories': categories,
        'products': products})


def product_home(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    moment_now=timezone.now()
    products = Product.objects.filter(available=True, init_dateTime__gte=moment_now).order_by('init_dateTime')[:5]
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = products.filter(category=category)
    
    # necessary for the shopping cart digit
    if not request.user.is_superuser:
        data = cartData(request)
        cartItems = data['cartItems']

        return render(request,
        'shop/product/listHome.html',
        {'category': category,
        'categories': categories,
        'products': products, 
        'cartItems': cartItems,})
    return render(request,
        'shop/product/listHome.html',
        {'category': category,
        'categories': categories,
        'products': products})

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
    id=id,
    slug=slug,
    available=True)
    # List of comments for this post (=posts that are not reclamations)
    comments = product.comments.filter(reclamation=False)
    # Form for users to comment
    form = CommentForm()
    dif=product.finish_dateTime-product.init_dateTime
    duracion = round(dif.total_seconds() / 3600, 2)
    # necessary for the shopping cart digit
    if not request.user.is_superuser:
        data = cartData(request)
        cartItems = data['cartItems']

        return render(request,
        'shop/product/detail.html',
        {'product': product,
        'comments': comments,
        'form': form, 
        'cartItems':cartItems,
        'duration':duracion})
    return render(request,
        'shop/product/detail.html',
        {'product': product,
        'comments': comments,
        'form': form,
        'duration':duracion})

@login_required
@require_POST
def product_comment(request, id,slug):
    product = get_object_or_404(Product,
    id=id,
    slug=slug,
    available=True)
    comment = None
    comments = product.comments.filter(reclamation=False)
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the product to the comment
        comment.product = product
        comment.name=request.user.username
        comment.email=request.user.email
        # Save the comment to the database
        comment.save()
        form = CommentForm()
        return redirect('/' + str(product.id) + '/' + str(product.slug))
    return render(request, 'shop/product/detail.html',
        {'product': product,
        'form': form,
        'comments': comments,
        'comment': comment})




#Seach filter 
def index(request):
    # Get the search query and filters from the request's POST data
    search_query = request.POST.get('search_query', '')
    subject_query = request.POST.get('subject_query', '')
    professor_query = request.POST.get('professor_query', '')

    # Start with all products
    products = Product.objects.all()

    # Apply filters based on search criteria
    if search_query:
        products = products.filter(Q(name__icontains=search_query) |
                                   Q(subject__name__icontains=search_query) |
                                   Q(professor__name__icontains=search_query))
    
    # Apply filters based on subject criteria
    if subject_query:
        products = products.filter(subject__name__icontains=subject_query)

    # Apply filters based on professor criteria
    if professor_query:
        products = products.filter(professor__name__icontains=professor_query)

    # Necessary for the shopping cart digit
    if not request.user.is_superuser:
        data = cartData(request)
        cartItems = data['cartItems']

        return render(request, 'shop/product/search_results.html', {
            'products': products,
            'search_query': search_query,
            'subject_query': subject_query,
            'professor_query': professor_query,
            'cartItems': cartItems,
        })
    
    return render(request, 'shop/product/search_results.html', {
            'products': products,
            'search_query': search_query,
            'subject_query': subject_query,
            'professor_query': professor_query
    })



#FILTER BY 3 CRITERIA

# views.py
from django.shortcuts import render
from .models import Product

def filter_products(request):
    min_price_filter = request.POST.get('min_price_filter')
    max_price_filter = request.POST.get('max_price_filter')
    subject_filter = request.POST.get('subject_filter')
    professor_filter = request.POST.get('professor_filter')

    products = Product.objects.all()

    if min_price_filter:
        products = products.filter(price__gte=min_price_filter)

    if max_price_filter:
        products = products.filter(price__lte=max_price_filter)

    if subject_filter:
        products = products.filter(subject__name__icontains=subject_filter)

    if professor_filter:
        products = products.filter(professor__name__icontains=professor_filter)

    context = {
        'products': products,
        'min_price_filter': min_price_filter,
        'max_price_filter': max_price_filter,
        'subject_filter': subject_filter,
        'professor_filter': professor_filter,
    }

    return render(request, 'shop/product/search_results.html', context)


def cart(request):
    if not request.user.is_superuser:
        data = cartData(request)
        cartItems = data['cartItems']
        items = data['items']
        order = data['order']

        context = {'items':items, 'order':order, 'cartItems':cartItems}
        
        return render(request, 'shop/cart.html', context)
    return render(request, 'shop/cart.html')

def updateItem(request):
    
    data = json.loads(request.body)
    
    productId = data['productID']
    action = data['action']

    print('action:', action, 'id', productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if product.quota <= 0:
        messages.error(request, 'La clase ya esta completa.')
    else:
        orders = Order.objects.filter(customer=customer, completed=True)
        has_bought_product = any(order.orderitem_set.filter(product=product).exists() for order in orders)
        if has_bought_product:
            messages.error(request, 'Este artículo ya ha sido comprado.')
        elif action == 'add' and has_bought_product == False:
            if orderItem.quantity < 1:
                orderItem.quantity += 1
            elif orderItem.quantity == 1:
                messages.error(request, 'Solo puedes reservar la misma clase una vez.')
        

    if action == 'remove':
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def checkout(request):
    if not request.user.is_superuser:
        data = cartData(request)
        cartItems = data['cartItems']
        items = data['items']
        order = data['order']
        print(items)
        print(order)
        fisico = False
        if not request.user.is_authenticated:
            for item in items:
                if (Product.objects.get(id = item['product']['id']).category.name == 'Fisico'):
                   fisico = True
            for item in items:
                product = Product.objects.get(id = item['product']['id'])
                if product.quota <= 0:
                    messages.error(request, 'La clase ya esta completa.')
                    return redirect('shop:cart')
        else:           
            for item in items:
                product = Product.objects.get(id = item.product.id)
                if product.quota <= 0:
                    messages.error(request, 'La clase ya esta completa.')
                    return redirect('shop:cart')

        context = {'items':items, 'order':order, 'cartItems':cartItems, 'fisico':fisico}
        return render(request, 'shop/checkout.html', context)

def process_payment(request):
    if request.method == 'POST':
        if request.user.is_authenticated:
            # Retrieve form data
            customer = request.user.customer
            order = get_object_or_404(Order, customer=customer, completed=False)
            items = order.orderitem_set.all()
            total = order.get_cart_total
            order_id = order.id
            code = order.code
            email = request.POST.get('email')
            name = request.POST.get('name')
            payment_method = request.POST.get('payment_method')
        else:
            # handle guest user situation:
            email = request.POST.get('email')
            name = request.POST.get('name')
            payment_method = request.POST.get('payment_method')
            
            data = cookieCart(request)
            items = data['items']

            # create a customer in the background, user won't see this
            customer, created = Customer.objects.get_or_create(
                email=email
            )
            customer.name = name
            customer.save()
            # create the Order from the cookie data
            order = Order.objects.create(
                customer = customer,
                completed = False
            )
            # create the OrderItems from the cookie data
            for item in items:
                product = Product.objects.get(id=item['product']['id'])
                orderItem = OrderItem.objects.create(
                    product=product,
                    order=order,
                    quantity=item['quantity']
                )

            items = order.orderitem_set.all()
            total = order.get_cart_total
            order_id = order.id
            code = order.code

        context = {
        'name': name,
        'total': total,
        'items': items,
        'payment_method': payment_method,
        'order_id': order_id,
        'email': email,
        'code': code
        }
        # Process the payment method
        if payment_method == 'Cash':
            # Handle Cash payment logic
            return redirect(f'/payment/completed/{order.id}/', context)
        elif payment_method == 'Stripe':
            # Handle Stripe payment logic
            return redirect(f'/payment/process/{order.id}/', context)
        else:
            messages.error(request, 'Invalid payment method selected.')
        
        


#seguimiento
def tracking(request):
    order = None
    items = None
    if request.method == 'POST':
        tracking_id = request.POST.get('tracking_id')
        try:
            order = Order.objects.get(tracking=tracking_id)
            items = order.orderitem_set.all()
        except Order.DoesNotExist:
            mensaje_error = 'No se encontró ningún pedido con este ID de seguimiento.'
            return render(request, 'shop/tracking.html', {'mensaje_error': mensaje_error})

    return render(request, 'shop/tracking.html', {'order': order , 'items':items})


def order_list(request):
    orders = Order.objects.all()
    order_items = OrderItem.objects.select_related('product').all()
    
    return render(request, 'shop/orders.html', {'orders': orders ,'order_items': order_items})


def change_state_order(request, order_id):
    order = get_object_or_404(Order, id=order_id)
    if request.method == 'POST':
        form = ChangeStateForm(request.POST, instance=order)
        if form.is_valid():
            form.save()
            return redirect('/order_list/')
    else:
        form = ChangeStateForm(instance=order)

    return render(request, 'shop/change_state.html', {'form': form, 'order': order})


def myorders(request):  
    if request.user.is_authenticated:
        user_orders = Order.objects.filter(customer=request.user.customer)
        return render(request, 'shop/myorders.html', {'user_orders': user_orders})  
    else:
        return render(request, 'shop/myorders.html', {'user_orders': None})  
    
def aboutUs(request):
    return render(request, 'shop/aboutUs.html')
