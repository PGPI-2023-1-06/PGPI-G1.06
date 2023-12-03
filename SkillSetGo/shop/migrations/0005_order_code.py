# Generated by Django 4.2.7 on 2023-12-01 23:24

from django.db import migrations, models
import shop.models


class Migration(migrations.Migration):
    dependencies = [
        ("shop", "0004_alter_order_customer"),
    ]

    operations = [
        migrations.AddField(
            model_name="order",
            name="code",
            field=models.CharField(
                blank=True, default=shop.models.get_code, editable=False, max_length=10
            ),
        ),
    ]
