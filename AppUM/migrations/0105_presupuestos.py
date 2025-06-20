# Generated by Django 5.0.6 on 2025-05-26 23:49

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppUM', '0104_alter_cliente_apellido_alter_cliente_nombre'),
    ]

    operations = [
        migrations.CreateModel(
            name='Presupuestos',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=300)),
                ('fecha', models.DateField()),
                ('archivo', models.FileField(blank=True, null=True, upload_to='documentacion/presupuestos/')),
                ('usuario', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='personal_presupuesto', to='AppUM.personal')),
            ],
        ),
    ]
