# Generated by Django 5.0.2 on 2024-07-23 00:53

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0005_remove_empleados_cargo_alter_mediciones_oxigeno_and_more'),
    ]

    operations = [
        migrations.AlterField(
            model_name='mediciones',
            name='piscina',
            field=models.ForeignKey(default='Eliminada', on_delete=django.db.models.deletion.DO_NOTHING, to='index.piscinas'),
        ),
    ]
