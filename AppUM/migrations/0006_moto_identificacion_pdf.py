# Generated by Django 5.0.6 on 2024-10-23 15:12

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppUM', '0005_remove_moto_matricula_matriculas'),
    ]

    operations = [
        migrations.AddField(
            model_name='moto',
            name='identificacion_pdf',
            field=models.FileField(blank=True, null=True, upload_to='motos/pdfs/'),
        ),
    ]
