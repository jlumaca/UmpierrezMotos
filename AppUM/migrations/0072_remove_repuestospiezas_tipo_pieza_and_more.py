# Generated by Django 5.0.6 on 2025-01-04 15:51

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppUM', '0071_remove_cuotasaccesorios_fecha_prox_pago'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='repuestospiezas',
            name='tipo_pieza',
        ),
        migrations.AddField(
            model_name='repuestospiezas',
            name='stock',
            field=models.IntegerField(null=True),
        ),
    ]
