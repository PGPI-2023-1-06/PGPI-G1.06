from django.http import HttpResponse, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render, redirect
from django.contrib.auth import authenticate, login
from django.urls import reverse
from django.contrib.auth.models import User
from .forms import LoginForm, ProductForm, UserRegistrationForm, CategoryForm, SubjetcForm, ProfessorForm ,UserProfileForm
from django.contrib.auth.decorators import login_required, user_passes_test
from django.views.decorators.http import require_POST
from django.http import HttpResponseBadRequest
from shop.models import Comment, Customer, Order, OrderItem, Product, Category, Subject, Professor
from shop.utils import cartData
from django.db.models import Sum



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
        data = cartData(request)
        cartItems = data['cartItems']

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
        product.image=form.data['image']
        product.save()
        return render(request, 'account/dashboard.html',
            {'product': product,
            'form': form})
    return render(request, 'account/administration/product.html', {'form':form})

def update_product_form(request, id):
    product = get_object_or_404(Product, pk=id)
    form = ProductForm(instance=product)
    form.product_id=id
    return render(request, 'account/administration/product_update.html', {'form': form,'product':product})


def update_product_post(request):
    product_initial = get_object_or_404(Product, pk=request.POST['id'])
    form = ProductForm(data=request.POST)
    if form.is_valid():
        product = form.save(commit=False)
        product.id=request.POST['id']
        if form.data['image'] != product_initial.image and form.data['image'] !='':
            product.image=form.data['image']
        else:
            product.image=product_initial.image
        product.created=product_initial.created
        product.save()

        return redirect('admin_product_list')
    
    return render(request, 'account/administration/product_update.html', {'form': form,'product':product_initial})




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

def update_category_form(request, id):
    category = get_object_or_404(Category, pk=id)
    form = CategoryForm(instance=category)
    form.category_id=id
    return render(request, 'account/administration/category_update.html', {'form': form,'category':category})


def update_category_post(request):
    category_initial = get_object_or_404(Category, id=request.POST['id'])
    form = CategoryForm(data=request.POST)
    if form.is_valid():
        category = form.save(commit=False)
        category.id=category_initial.id
        category.save()

        return redirect('admin_category_list')
    
    return render(request, 'account/administration/category_update.html', {'form': form,'category':category_initial})

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

def update_subject_form(request, id):
    subject = get_object_or_404(Subject, pk=id)
    form = SubjetcForm(instance=subject)
    form.subject_id=id
    return render(request, 'account/administration/subject_update.html', {'form': form,'subject':subject})


def update_subject_post(request):
    subject_initial = get_object_or_404(Subject, id=request.POST['id'])
    form = SubjetcForm(data=request.POST)
    if form.is_valid():
        subject = form.save(commit=False)
        subject.id=subject_initial.id
        subject.save()

        return redirect('admin_subject_list')
    
    return render(request, 'account/administration/subject_update.html', {'form': form,'subject':subject_initial})

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

def update_professor_form(request, id):
    professor = get_object_or_404(Professor, pk=id)
    form = ProfessorForm(instance=professor)
    form.professor_id=id
    return render(request, 'account/administration/professor_update.html', {'form': form,'professor':professor})


def update_professor_post(request):
    professor_initial = get_object_or_404(Professor, id=request.POST['id'])
    form = ProfessorForm(data=request.POST)
    if form.is_valid():
        professor = form.save(commit=False)
        professor.id=professor_initial.id
        professor.save()

        return redirect('admin_professor_list')
    
    return render(request, 'account/administration/professor_update.html', {'form': form,'professor':professor_initial})

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
            return redirect('login')
    else:
        user_form = UserRegistrationForm()
    return render(request,'account/register.html',{'user_form': user_form})

@login_required
def edit_profile(request):
    if request.method == 'POST':
        form = UserProfileForm(request.POST, instance=request.user)
        if form.is_valid():
            form.save()
            return redirect('dashboard')  # Redirige a la página de perfil
    else:
        form = UserProfileForm(instance=request.user)

    return render(request, 'account/edit_profile.html', {'form': form})



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


#Admin views for updating and deleting products/subjects/categories/professors
@user_passes_test(lambda u: u.is_superuser)
def admin_product_list(request):
    products = Product.objects.all()
    return render(request, 'account/administration/admin_product_list.html', {'products': products})


def delete_product(request, product_id):
    product = get_object_or_404(Product, pk=product_id)
    if request.method == 'POST':
        product.delete()
        # Redirect to the product list page after deletion
        return redirect('admin_product_list')
    # Handle GET requests or other conditions if needed
    return render(request, 'account/administration/delete_confirmation.html', {'product': product})

@user_passes_test(lambda u: u.is_superuser)
def admin_category_list(request):
    categories = Category.objects.all()
    return render(request, 'account/administration/admin_category_list.html', {'categories': categories})

def delete_category(request, category_id):
    category = get_object_or_404(Category, pk=category_id)
    if request.method == 'POST':
        category.delete()
        # Redirect to the product list page after deletion
        return redirect('admin_category_list')
    # Handle GET requests or other conditions if needed
    return render(request, 'account/administration/delete_confirmation.html', {'category': category})

@user_passes_test(lambda u: u.is_superuser)
def admin_subject_list(request):
    subjects = Subject.objects.all()
    return render(request, 'account/administration/admin_subject_list.html', {'subjects': subjects})

def delete_subject(request, subject_id):
    subject = get_object_or_404(Subject, pk=subject_id)
    if request.method == 'POST':
        subject.delete()
        # Redirect to the product list page after deletion
        return redirect('admin_subject_list')
    # Handle GET requests or other conditions if needed
    return render(request, 'account/administration/delete_confirmation.html', {'subject': subject})

@user_passes_test(lambda u: u.is_superuser)
def admin_professor_list(request):
    professors = Professor.objects.all()
    return render(request, 'account/administration/admin_professor_list.html', {'professors': professors})

def delete_professor(request, professor_id):
    professor = get_object_or_404(Professor, pk=professor_id)
    if request.method == 'POST':
        professor.delete()
        # Redirect to the product list page after deletion
        return redirect('admin_professor_list')
    # Handle GET requests or other conditions if needed
    return render(request, 'account/administration/delete_confirmation.html', {'professor': professor})


#Gestion de ventas
def users_management(request):
    users = User.objects.all()
    return render(request, 'account/administration/users_management.html', {'users': users})

def delete_user(request, user_id):
    if request.method == 'POST':
        user = get_object_or_404(User, id=user_id)
        user.delete()
        return HttpResponseRedirect(reverse('users_management'))

    return render(request, 'account/dashboard.html', {'section': 'dashboard'})

def class_history(request):
    customers = Customer.objects.all()
    for customer in customers:
        completed_orders = customer.orders.filter(completed=True)
        return render(request, 'account/administration/class_history.html', {'customers': customers})
    
@login_required
def sales_management(request):
    if request.user.is_superuser:
        return render(request, 'account/administration/sales_management.html')
    else:
        return render(request, 'account/dashboard.html', {'section': 'dashboard'})
    
def sales_report(request):
    completed_orders = Order.objects.filter(completed=True)
    total_sales = sum(order.get_cart_total for order in completed_orders)
    sales_per_product = OrderItem.objects.values('product__name').annotate(total=Sum('quantity')).order_by('-total')    
    return render(request, 'account/administration/sales_report.html', {'total_sales': total_sales, 'sales_per_product': sales_per_product})