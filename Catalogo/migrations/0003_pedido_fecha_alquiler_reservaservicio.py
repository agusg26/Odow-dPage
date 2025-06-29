# Generated by Django 5.2.3 on 2025-06-26 01:37

import django.db.models.deletion
import django.utils.timezone
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('Catalogo', '0002_cerveza_porcentaje_alcohol'),
    ]

    operations = [
        migrations.AddField(
            model_name='pedido',
            name='fecha_alquiler',
            field=models.DateField(default=django.utils.timezone.now),
        ),
        migrations.CreateModel(
            name='ReservaServicio',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('fecha', models.DateField()),
                ('servicio', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='Catalogo.servicio')),
            ],
        ),
    ]
