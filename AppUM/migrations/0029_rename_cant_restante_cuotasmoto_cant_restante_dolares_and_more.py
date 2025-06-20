# Generated by Django 5.0.6 on 2024-11-26 18:48

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('AppUM', '0028_rename_fecha_cuota_cuotasmoto_fecha_pago_and_more'),
    ]

    operations = [
        migrations.RenameField(
            model_name='cuotasmoto',
            old_name='cant_restante',
            new_name='cant_restante_dolares',
        ),
        migrations.RenameField(
            model_name='cuotasmoto',
            old_name='valor_pago',
            new_name='cant_restante_pesos',
        ),
        migrations.AddField(
            model_name='cuotasmoto',
            name='moneda',
            field=models.CharField(default=True, max_length=10, null=True),
        ),
        migrations.AddField(
            model_name='cuotasmoto',
            name='observaciones',
            field=models.TextField(blank=True, null=True),
        ),
        migrations.AddField(
            model_name='cuotasmoto',
            name='precio_dolar',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='cuotasmoto',
            name='valor_pago_dolares',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
        migrations.AddField(
            model_name='cuotasmoto',
            name='valor_pago_pesos',
            field=models.DecimalField(decimal_places=2, default=0, max_digits=10),
        ),
    ]
