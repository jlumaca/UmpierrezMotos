# Generated by Django 5.0.6 on 2024-12-27 13:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppUM', '0057_remove_cliente_calle_remove_cliente_ciudad_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='cliente',
            name='domicilio',
            field=models.CharField(blank=True, max_length=500),
        ),
    ]
