import json
from django.shortcuts import render, get_object_or_404
from django.db.models import Q  
from django.views.decorators.http import require_POST
from .forms import CommentForm
from .models import Category, Product, Professor, Subject, Order, OrderItem ,Comment
from django.http import JsonResponse


# Create your views here.

def product_list(request, category_slug=None):
    category = None
    categories = Category.objects.all()
    products = Product.objects.filter(available=True)
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
    # List of active comments for this post
    comments = product.comments.filter(active=True)
    # Form for users to comment
    form = CommentForm()

    return render(request,
    'shop/product/detail.html',
    {'product': product,
    'comments': comments,
    'form': form})


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

    return render(request, 'shop/product/search_results.html', {
        'products': products,
        'search_query': search_query,
        'subject_query': subject_query,
        'professor_query': professor_query,
    })

def cart(request):
    if request.user.is_authenticated:
        customer = request.user
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
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
    order, created = Order.objects.get_or_create(customer=customer, completed=False)

    orderItem, created = OrderItem.objects.get_or_create(order=order, product=product)

    if action == 'remove':
        orderItem.delete()

    
    return JsonResponse('Item was added', safe=False)

def checkout(request):
    if request.user.is_authenticated:
        customer = request.user.customer
        order, created = Order.objects.get_or_create(customer=customer, completed=False)
        items = order.orderitem_set.all()
    else:
        items = []
        order = {'get_cart_total':0, 'get_cart_items':0}

    context = {'items':items, 'order':order}
    return render(request, 'shop/checkout.html', context)


