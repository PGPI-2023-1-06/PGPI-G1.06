import os
os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'SkillSetGo.settings')  # Change 'your_project_name' to your actual project name

import django
django.setup()

from shop.models import Category, Professor, Subject, Product
from django.utils.text import slugify
from faker import Faker
import random
from datetime import datetime, timedelta

fake = Faker()

def populate():
    populate_categories()
    populate_professors()
    populate_subjects()
    populate_products()

    # Print out what we have added to the user.
    for c in Category.objects.all():
        for p in Product.objects.filter(category=c):
            print("- {0} - {1}".format(str(c), str(p)))

def populate_categories():
    categories_data = [
        {'name': 'Online', 'slug': 'online'},
        {'name': 'Fisico', 'slug': 'fisico'},
    ]
    for category_data in categories_data:
        name = category_data['name']
        slug = category_data['slug']
        Category.objects.get_or_create(name=name, slug=slug)

def populate_professors():
    for i in range(1, 6):
        name = fake.first_name()
        surname = fake.last_name()
        slug = slugify(f'{name} {surname}')
        Professor.objects.get_or_create(name=name, surname=surname, slug=slug)

def populate_subjects():
    subjects_data = [
        {'name': 'Inglés', 'slug': 'ingles'},
        {'name': 'Lengua', 'slug': 'lengua'},
        {'name': 'Matemáticas', 'slug': 'matemáticas'},
    ]

    for subject_data in subjects_data:
        name = subject_data['name']
        slug = subject_data['slug']
        Subject.objects.get_or_create(name=name, slug=slug)

def populate_products():
    categories = Category.objects.all()
    professors = Professor.objects.all()
    subjects = Subject.objects.all()



    products_data = [
        {
            'category': random.choice(categories),
            'professor': random.choice(professors),
            'subject': random.choice(subjects),
            'name': '01.13',
            'slug': '01-13',
            'image': 'clase1.jpg',
            'description': fake.paragraph(),
            'price': round(random.uniform(10, 100), 2),
            'available': random.choice([True, False]),
            'init_dateTime': fake.date_time_this_year(),
            'finish_dateTime': fake.date_time_this_year() + timedelta(days=random.randint(7, 30)),
            'quota': random.randint(1,30),
        },
        {
            'category': random.choice(categories),
            'professor': random.choice(professors),
            'subject': random.choice(subjects),
            'name': '02.24 ',
            'slug': '02-24',
            'image':  'class.jpeg' ,
            'description': fake.paragraph(),
            'price': round(random.uniform(10, 100), 2),
            'available': random.choice([True, False]),
            'init_dateTime': fake.date_time_this_year(),
            'finish_dateTime': fake.date_time_this_year() + timedelta(days=random.randint(7, 30)),
            'quota': random.randint(1,30),
        },
        {
            'category': random.choice(categories),
            'professor': random.choice(professors),
            'subject': random.choice(subjects),
            'name': '03.05',
            'slug': '03-05',
            'image':  'clase1.jpg' ,
            'description': fake.paragraph(),
            'price': round(random.uniform(10, 100), 2),
            'available': random.choice([True, False]),
            'init_dateTime': fake.date_time_this_year(),
            'finish_dateTime': fake.date_time_this_year() + timedelta(days=random.randint(7, 30)),
            'quota': random.randint(1,30),
        },
        {
            'category': random.choice(categories),
            'professor': random.choice(professors),
            'subject': random.choice(subjects),
            'name': '04.16',
            'slug': '04-16',
            'image':  'class.jpeg',
            'description': fake.paragraph(),
            'price': round(random.uniform(10, 100), 2),
            'available': random.choice([True, False]),
            'init_dateTime': fake.date_time_this_year(),
            'finish_dateTime': fake.date_time_this_year() + timedelta(days=random.randint(7, 30)),
            'quota': random.randint(1,30),
        },
        {
            'category': random.choice(categories),
            'professor': random.choice(professors),
            'subject': random.choice(subjects),
            'name': '05.27',
            'slug': '05-27',
            'image':  'clase1.jpg' ,
            'description': fake.paragraph(),
            'price': round(random.uniform(10, 100), 2),
            'available': random.choice([True, False]),
            'init_dateTime': fake.date_time_this_year(),
            'finish_dateTime': fake.date_time_this_year() + timedelta(days=random.randint(7, 30)),
            'quota': random.randint(1,30),
        },
        # Add more products as needed
    ]

    for product_data in products_data:
        Product.objects.get_or_create(**product_data)

if __name__ == '__main__':
    print("Starting population script...")
    populate()
