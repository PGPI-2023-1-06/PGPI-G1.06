from django.shortcuts import render, get_object_or_404
from .models import Category, Product, Professor, Subject, Comment
from .forms import CommentForm
from django.views.decorators.http import require_POST

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
