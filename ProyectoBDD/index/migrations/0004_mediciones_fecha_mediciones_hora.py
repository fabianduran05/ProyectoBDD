# Generated by Django 5.0.2 on 2024-07-13 23:14

import datetime
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('index', '0003_alter_parametros_unidad'),
    ]

    operations = [
        migrations.AddField(
            model_name='mediciones',
            name='fecha',
            field=models.DateField(default=datetime.date.today),
        ),
        migrations.AddField(
            model_name='mediciones',
            name='hora',
            field=models.TimeField(default=datetime.time(0, 0)),
        ),
    ]
