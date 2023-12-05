from django.db import models
from django.urls import reverse
from django.contrib.auth.models import User
from django.utils.crypto import get_random_string

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    class Meta:
        ordering = ['name']
        indexes = [
        models.Index(fields=['name']),
        ]
        verbose_name = 'category'
        verbose_name_plural = 'categories'
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_list_by_category',args=[self.slug])
    

class Professor(models.Model):
    name = models.CharField(max_length=200)
    surname = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    class Meta:
        ordering = ['name']
        indexes = [
        models.Index(fields=['name']),
        ]
        verbose_name = 'professor'
        verbose_name_plural = 'professors'
    def __str__(self):
        return self.name
    
class Subject(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    class Meta:
        ordering = ['name']
        indexes = [
        models.Index(fields=['name']),
        ]
        verbose_name = 'subject'
        verbose_name_plural = 'subjects'
    def __str__(self):
        return self.name

class Product(models.Model):
    category = models.ForeignKey(Category,related_name='products',on_delete=models.CASCADE)
    professor = models.ForeignKey(Professor,related_name='products',on_delete=models.CASCADE)
    subject = models.ForeignKey(Subject,related_name='products',on_delete=models.CASCADE)
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200)
    image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True , default="noimage.jpg")
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    available = models.BooleanField(default=True)
    init_dateTime = models.DateTimeField()
    finish_dateTime = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    quota =  models.IntegerField(default=20)
    class Meta:
        ordering = ['name']
        indexes = [
        models.Index(fields=['id', 'slug']),
        models.Index(fields=['name']),
        models.Index(fields=['-created']),
        ]
    def __str__(self):
        return self.name
    
    def get_absolute_url(self):
        return reverse('shop:product_detail',args=[self.id, self.slug])

    

class Comment(models.Model):
    product = models.ForeignKey(Product,on_delete=models.CASCADE,related_name='comments')
    name = models.CharField(max_length=80)
    email = models.EmailField()
    body = models.TextField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
    active = models.BooleanField(default=True)
    reclamation = models.BooleanField(default=False)

    class Meta:
        ordering = ['created']
        indexes = [
        models.Index(fields=['created']),
        ]

    def __str__(self):
        return f'Comment by {self.name} on {self.product}'
    
    def get_absolute_url(self):
        return reverse('shop:product_comment',args=[self.id, self.slug])


class Customer(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, null=True, blank=True)
    name = models.CharField(max_length=200, null=True)
    email = models.EmailField(max_length=200, null=True)

    def __str__(self):
        return self.name

def get_code():
        code = get_random_string(length=8)
        return code

def get_tracking_id():
    return get_random_string(length=10, allowed_chars='abcdefghijklmnopqrstuvwxyz0123456789')

class Order(models.Model):
    customer = models.ForeignKey(Customer, on_delete=models.SET_NULL, null=True, blank=True, related_name='orders')
    date_ordered = models.DateTimeField(auto_now_add=True)
    completed = models.BooleanField(default=False) #to know if products can still be added to the order
    code = models.CharField(
        max_length = 10,
        blank=True,
        editable=False,
        default=get_code)
    #seguimiento
    tracking = models.CharField(
        max_length=10,
        blank=True,
        editable=False,
        default=get_tracking_id,
        unique=True  # Para asegurar que cada ID de seguimiento sea único
    )


    def __str__(self):
        return str(self.id)

    @property 
    def get_cart_total(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.get_total for item in orderitems])
        return total

    @property 
    def get_cart_items(self):
        orderitems = self.orderitem_set.all()
        total = sum([item.quantity for item in orderitems])
        return total

    @property
    def is_in_person(self):
        orderitems = self.orderitem_set.all()
        cat = True
        for item in orderitems:
            if item.product.category.name == 'Online':
                cat = False
        return cat

class OrderItem(models.Model):
    product = models.ForeignKey(Product, on_delete=models.SET_NULL, blank=True, null=True)
    order = models.ForeignKey(Order, on_delete=models.SET_NULL, blank=True, null=True)
    quantity = models.IntegerField(default=0, null=True, blank=True)
    date_added = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return str(self.product.name)

    @property
    def get_total(self):
        total = self.product.price * self.quantity
        return total

