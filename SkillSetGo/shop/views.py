from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Professor, Subject
from django.db.models import Q  

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

    return render(request,
    'shop/product/detail.html',
    {'product': product})


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