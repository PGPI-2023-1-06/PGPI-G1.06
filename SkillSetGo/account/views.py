from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login

from shop.models import Comment, Customer, Order
from .forms import LoginForm, UserRegistrationForm
from django.contrib.auth.decorators import login_required
from django.contrib.auth.models import User

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

#Gestion de ventas
def sales_management(request):
    users = User.objects.all()
    return render(request, 'account/administration/sales_management.html', {'users': users})