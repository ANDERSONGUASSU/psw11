# Generated by Django 5.0.7 on 2024-08-11 10:33

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresarios', '0004_documento'),
    ]

    operations = [
        migrations.CreateModel(
            name='Metricas',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('titulo', models.CharField(max_length=30)),
                ('valor', models.FloatField()),
                ('empresa', models.ForeignKey(on_delete=django.db.models.deletion.DO_NOTHING, to='empresarios.empresas')),
            ],
        ),
    ]
