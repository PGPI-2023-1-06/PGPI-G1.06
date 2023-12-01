from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth import authenticate, login


from .forms import LoginForm, ProductForm, UserRegistrationForm, CategoryForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest


def user_login(request):
    if request.method == 'POST':
        form = LoginForm(request.POST)
        if form.is_valid():
            cd = form.cleaned_data
            user = authenticate(request, username=cd['username'],password=cd['password'])
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
    else:
        return HttpResponseBadRequest("Error en el formulario. Por favor, corrige los errores.")
    return render(request, 'account/dashboard.html',
        {'product': product,
        'form': form})

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
            return render(request, 'account/register_done.html',{'new_user': new_user})
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})