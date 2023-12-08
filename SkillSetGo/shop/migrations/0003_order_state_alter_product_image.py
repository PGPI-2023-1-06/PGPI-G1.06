# Generated by Django 4.2.7 on 2023-12-08 13:21

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('shop', '0002_alter_category_slug_alter_product_image_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='order',
            name='state',
            field=models.CharField(choices=[('en_espera', 'En Espera'), ('pendiente_pago', 'Pendiente de pago'), ('pagado', 'Pagado')], default='en_espera', max_length=20),
        ),
        migrations.AlterField(
            model_name='product',
            name='image',
            field=models.ImageField(blank=True, default='noimage.jpg', upload_to='products/%Y/%m/%d'),
        ),
    ]
