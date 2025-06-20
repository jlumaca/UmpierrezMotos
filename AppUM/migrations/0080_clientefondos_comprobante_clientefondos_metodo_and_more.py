# Generated by Django 5.0.6 on 2025-01-14 13:02

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppUM', '0079_rename_ingreso_clientefondos_ingreso_dolares_and_more'),
    ]

    operations = [
        migrations.AddField(
            model_name='clientefondos',
            name='comprobante',
            field=models.FileField(blank=True, null=True, upload_to='documentacion/comprobantes/'),
        ),
        migrations.AddField(
            model_name='clientefondos',
            name='metodo',
            field=models.CharField(blank=True, max_length=20),
        ),
        migrations.AddField(
            model_name='clientefondos',
            name='tipo',
            field=models.CharField(default=True, max_length=10, null=True),
        ),
    ]
