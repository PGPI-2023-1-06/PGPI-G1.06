from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login
from .forms import LoginForm, ProductForm, UserRegistrationForm, CategoryForm, SubjetcForm, ProfessorForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest
from shop.models import Comment, Customer, Order


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['email'],password=cd['password'])
            if user is not None:
                if user.is_active:
                    login(request, user)
                    return HttpResponse('Authenticated successfully')
                else:
                    return HttpResponse('Disabled account')
            else:
                return HttpResponse('Invalid login')
    else:
        form = LoginForm()
    return render(request, 'account/login.html', {'form': form})


@login_required
def dashboard(request):

    # necessary for the shopping cart digit
    if not request.user.is_superuser:
        if request.user.is_authenticated:
            customer = request.user.customer
            order, created = Order.objects.get_or_create(customer=customer, completed=False)
            items = order.orderitem_set.all()
            cartItems = order.get_cart_items
        else:
            items = []
            order = {'get_cart_total':0, 'get_cart_items':0}
            cartItems = order['get_cart_items']
        return render(request, 'account/dashboard.html', {'section': 'dashboard', 'cartItems': cartItems})
    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

#Vistas para administrar productos
@user_passes_test(lambda u: u.is_superuser)
def product_form(request):
    form = ProductForm()
    return render(request, 'account/administration/product.html', {'form':form})

@require_POST
def product_post(request):
    product = None
    form = ProductForm(data=request.POST)
    if form.is_valid():
        product = form.save(commit=False)
        product.save()
        return render(request, 'account/dashboard.html',
            {'product': product,
            'form': form})
    return render(request, 'account/administration/product.html', {'form':form})

#Vistas para administrar categorias
@user_passes_test(lambda u: u.is_superuser)
def category_form(request):
    form = CategoryForm()
    return render(request, 'account/administration/category.html', {'form':form})

@require_POST
def category_post(request):
    category = None
    form = CategoryForm(data=request.POST)
    if form.is_valid():
        category = form.save(commit=False)
        category.save()
    else:
        return HttpResponseBadRequest("Error en el formulario. Por favor, corrige los errores.")
    return render(request, 'account/dashboard.html',
        {'category': category,
        'form': form})

#Vistas para administrar asignaturas
@user_passes_test(lambda u: u.is_superuser)
def subject_form(request):
    form = SubjetcForm()
    return render(request, 'account/administration/subject.html', {'form':form})

@require_POST
def subject_post(request):
    subject = None
    form = SubjetcForm(data=request.POST)
    if form.is_valid():
        subject = form.save(commit=False)
        subject.save()
    else:
        return HttpResponseBadRequest("Error en el formulario. Por favor, corrige los errores.")
    return render(request, 'account/dashboard.html',
        {'subject': subject,
        'form': form})

#Vistas para administrar profesores
@user_passes_test(lambda u: u.is_superuser)
def professor_form(request):
    form = ProfessorForm()
    return render(request, 'account/administration/professor.html', {'form':form})

@require_POST
def professor_post(request):
    professor = None
    form = ProfessorForm(data=request.POST)
    if form.is_valid():
        professor = form.save(commit=False)
        professor.save()
    else:
        return HttpResponseBadRequest("Error en el formulario. Por favor, corrige los errores.")
    return render(request, 'account/dashboard.html',
        {'professor': professor,
        'form': form})

def register(request):
    if request.method == 'POST':
        user_form = UserRegistrationForm(request.POST)
        if user_form.is_valid():
            # Create a new user object but avoid saving it yet
            new_user = user_form.save(commit=False)
            # Set the chosen password
            new_user.set_password(
            user_form.cleaned_data['password'])
            # Save the User object
            new_user.save()
            # Create a customer object to link orders to users
            customer = Customer.objects.create(user=new_user, name=new_user.username, email=new_user.email)
            customer.save()
            return render(request, 'account/register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})


#gestion de reclamaciones
def reclamations_list(request):
    reclamations = Comment.objects.filter(reclamation=True)

        
    return render(request,
    'account/administration/reclamation.html',
    {'reclamations': reclamations})

#Cierre de reclamaciones
def close_reclamation(request,id):
    Comment.objects.filter(id=id).update(reclamation=False)
        
    return render(request,
    'account/dashboard.html',
    {'section': 'dashboard'})


def order_list(request):
    order = Order.objects.all()
    return render(request, 'account/administration/orders.html', {'order': order})

