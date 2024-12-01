# Generated by Django 5.1.1 on 2024-10-27 01:43

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cliente', '0002_initial'),
        ('fornecedor', '0002_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='Pedido',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('EM_ANDAMENTO', 'Em andamento'), ('CONCLUIDO', 'Concluído'), ('CANCELADO', 'Cancelado')], default='EM_ANDAMENTO', max_length=20)),
                ('total', models.FloatField(default=0)),
                ('data_venda', models.DateField()),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('quantidade', models.PositiveIntegerField()),
                ('descricao', models.CharField(editable=False, max_length=255)),
                ('prazo_entrega', models.DateField(editable=False)),
                ('cliente', models.ForeignKey(blank=True, on_delete=django.db.models.deletion.CASCADE, to='cliente.cliente')),
                ('fornecedor', models.ForeignKey(editable=False, on_delete=django.db.models.deletion.CASCADE, to='fornecedor.fornecedor')),
            ],
        ),
    ]
