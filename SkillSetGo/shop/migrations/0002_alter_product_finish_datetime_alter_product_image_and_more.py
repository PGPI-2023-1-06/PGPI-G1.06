# Generated by Django 4.2.7 on 2023-11-25 15:44

from django.db import migrations, models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0001_initial"),
    ]

    operations = [
        migrations.AlterField(
            model_name="product",
            name="finish_dateTime",
            field=models.DateTimeField(),
        ),
        migrations.AlterField(
            model_name="product",
            name="image",
            field=models.ImageField(
                blank=True,
                default="../media/noimage.jpg",
                upload_to="products/%Y/%m/%d",
            ),
        ),
        migrations.AlterField(
            model_name="product",
            name="init_dateTime",
            field=models.DateTimeField(),
        ),
    ]
