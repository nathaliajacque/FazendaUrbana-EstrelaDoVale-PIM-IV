# Generated by Django 5.1.1 on 2024-10-16 02:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('produto', '0001_initial'),
    ]

    operations = [
        migrations.AlterField(
            model_name='produto',
            name='solucao_nutritiva',
            field=models.TextField(),
        ),
    ]