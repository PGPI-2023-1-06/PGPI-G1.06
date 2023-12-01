import json
from django.shortcuts import render, get_object_or_404
from django.db.models import Q  
from django.views.decorators.http import require_POST
from .forms import CommentForm
from .models import Category, Product, Professor, Subject, Customer, Order, OrderItem ,Comment
from django.http import JsonResponse
from django.urls import reverse
from django.shortcuts import render, redirect
from django.contrib import messages
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.utils.html import strip_tags


# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
    if category_slug:
        category = get_object_or_404(Category,slug=category_slug)
        products = products.filter(category=category)
    
    # necessary for the shopping cart digit
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    
    return render(request,
    'shop/product/list.html',
    {'category': category,
    'categories': categories,
    'products': products, 
    'cartItems': cartItems,})

def product_detail(request, id, slug):
    product = get_object_or_404(Product,
    id=id,
    slug=slug,
    available=True)
    # List of active comments for this post
    comments = product.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    # necessary for the shopping cart digit
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    return render(request,
    'shop/product/detail.html',
    {'product': product,
    'comments': comments,
    'form': form, 
    'cartItems':cartItems})


@require_POST
def product_comment(request, id,slug):
    product = get_object_or_404(Product,
    id=id,
    slug=slug,
    available=True)
    comment = None
    # A comment was posted
    form = CommentForm(data=request.POST)
    if form.is_valid():
        # Create a Comment object without saving it to the database
        comment = form.save(commit=False)
        # Assign the product to the comment
        comment.product = product
        comment.name=request.user.username
        comment.email=request.user.email
        if comment.reclamation==True:
            comment.active=False
        # Save the comment to the database
        comment.save()
    return render(request, 'shop/product/comment.html',
        {'product': product,
        'form': form,
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
    
    if subject_query:
        products = products.filter(subject__name__icontains=subject_query)

    if professor_query:
        products = products.filter(professor__name__icontains=professor_query)

    # necessary for the shopping cart digit
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    return render(request, 'shop/product/search_results.html', {
        'products': products,
        'search_query': search_query,
        'subject_query': subject_query,
        'professor_query': professor_query,
        'cartItems':cartItems,
    })

def cart(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'shop/cart.html', context)

def updateItem(request):
    
    data = json.loads(request.body)
    
    productId = data['productID']
    action = data['action']

    print('action:', action, 'id', productId)
    customer = request.user.customer
    product = Product.objects.get(id=productId)
    order, created = Order.objects.get_or_create(customer=customer, completed=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'add':
        orderItem.quantity = orderItem.quantity + 1
    elif action == 'remove':
        orderItem.quantity = orderItem.quantity - 1

    orderItem.save()

    if orderItem.quantity <= 0:
        orderItem.delete()

    return JsonResponse('Item was added', safe=False)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
        cartItems = order.get_cart_items
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}
        cartItems = order['get_cart_items']

    context = {'items':items, 'order':order, 'cartItems':cartItems}
    return render(request, 'shop/checkout.html', context)
    
def enviar_correo(name, total, items, payment_method, order_id, email, code):
    subject = 'Your SkillSetGo Order Details'
    from_email = 'skillsetgo4@gmail.com'
    to_email = [email]
    order = get_object_or_404(Order, pk=order_id)

    context = {
        'name': name,
        'total': total,
        'items': items,
        'payment_method': payment_method,
        'order': order,
        'code': code,
        }

    html_message = render_to_string('payment/completed.html', context)
    plain_message = strip_tags(html_message)

    send_mail(subject, plain_message, from_email, to_email, html_message=html_message)

def process_payment(request):
    if request.method == 'POST':
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

        # Process the payment method
        if payment_method == 'Cash':
            # Handle Cash payment logic
            context = {'items':items, 'order':order}
            enviar_correo(name, total, items, payment_method, order_id, email, code)
            return redirect(f'/payment/completed/{order.id}/')
        elif payment_method == 'Stripe':
            # Handle Stripe payment logic
            enviar_correo(name, total, items, payment_method, order_id, email, code)
            return redirect(f'/payment/process/{order.id}/')
        else:
            messages.error(request, 'Invalid payment method selected.')
        

