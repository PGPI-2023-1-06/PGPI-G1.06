from django.db import models
from django.urls import reverse

# Create your models here.
class Category(models.Model):
    name = models.CharField(max_length=200)
    slug = models.SlugField(max_length=200,
    unique=True)
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
    slug = models.SlugField(max_length=200,
    unique=True)
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
    slug = models.SlugField(max_length=200,
    unique=True)
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
    image = models.ImageField(upload_to='products/%Y/%m/%d',blank=True,default='../media/noimage.jpg')
    description = models.TextField(blank=True)
    price = models.DecimalField(max_digits=10,decimal_places=2)
    available = models.BooleanField(default=True)
    init_dateTime = models.DateTimeField()
    finish_dateTime = models.DateTimeField()
    created = models.DateTimeField(auto_now_add=True)
    updated = models.DateTimeField(auto_now=True)
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