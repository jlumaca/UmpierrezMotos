# Generated by Django 5.0.6 on 2024-12-11 16:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppUM', '0042_servicios_mecanicosservicios_tareasservicios'),
    ]

    operations = [
        migrations.AddField(
            model_name='servicios',
            name='dias',
            field=models.IntegerField(default=0),
        ),
    ]
