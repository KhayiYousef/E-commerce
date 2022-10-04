# Generated by Django 3.2 on 2021-05-28 18:28

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0012_auto_20210528_2020'),
    ]

    operations = [
        migrations.AlterField(
            model_name='order',
            name='details',
            field=models.ManyToManyField(through='store.OrderDetails', to='store.Produit'),
        ),
        migrations.AlterField(
            model_name='userprofile',
            name='product_favorites',
            field=models.ManyToManyField(to='store.Produit'),
        ),
    ]
