# Generated by Django 5.0.6 on 2024-11-08 12:39

from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ('AppUM', '0017_alter_clientetelefono_telefono'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='clientecorreo',
            name='activo',
        ),
        migrations.RemoveField(
            model_name='clientetelefono',
            name='activo',
        ),
    ]
