# Generated by Django 4.1 on 2024-11-15 00:41

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('fornecedor', '0003_alter_fornecedor_numero'),
    ]

    operations = [
        migrations.AlterField(
            model_name='fornecedor',
            name='numero',
            field=models.PositiveBigIntegerField(),
        ),
    ]