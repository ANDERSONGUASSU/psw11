# Generated by Django 5.0.7 on 2024-08-08 11:34

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('empresarios', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='empresas',
            name='estagio',
            field=models.TextField(choices=[('I', 'Tenho apenas uma idea'), ('MVP', 'Possuo um MVP'), ('MVPP', 'Possuo um MVP com clientes pagantes'), ('E', 'Empresa pronta para escalar')], default='I', max_length=4),
        ),
    ]