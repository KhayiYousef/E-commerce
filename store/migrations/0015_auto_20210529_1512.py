# Generated by Django 3.2 on 2021-05-29 13:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('store', '0014_auto_20210528_2030'),
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
