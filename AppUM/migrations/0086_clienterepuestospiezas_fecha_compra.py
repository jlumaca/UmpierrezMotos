# Generated by Django 5.0.6 on 2025-01-20 21:04

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppUM', '0085_clienterepuestospiezas'),
    ]

    operations = [
        migrations.AddField(
            model_name='clienterepuestospiezas',
            name='fecha_compra',
            field=models.DateField(null=True),
        ),
    ]
