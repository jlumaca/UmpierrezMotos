# Generated by Django 5.0.6 on 2024-10-23 12:25

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppUM', '0004_alter_moto_matricula'),
    ]

    operations = [
        migrations.RemoveField(
            model_name='moto',
            name='matricula',
        ),
        migrations.CreateModel(
            name='Matriculas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('matricula', models.CharField(max_length=20, unique=True)),
                ('activo', models.BooleanField()),
                ('moto', models.ForeignKey(null=True, on_delete=django.db.models.deletion.CASCADE, related_name='moto', to='AppUM.moto')),
            ],
        ),
    ]
