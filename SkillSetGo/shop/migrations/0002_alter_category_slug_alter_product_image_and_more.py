# Generated by Django 4.2.7 on 2023-12-05 15:37

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='category',
            name='slug',
            field=models.SlugField(max_length=200),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, upload_to='products/%Y/%m/%d'),
        ),
        migrations.AlterField(
            model_name='professor',
            name='slug',
            field=models.SlugField(max_length=200),
        ),
        migrations.AlterField(
            model_name='subject',
            name='slug',
            field=models.SlugField(max_length=200),
        ),
    ]
