# Generated by Django 5.0.6 on 2024-11-20 14:22

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppUM', '0024_remove_comprasventas_cantidad_cuotas_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='comprasventas',
            name='forma_de_pago',
            field=models.TextField(blank=True, null=True),
        ),
    ]
