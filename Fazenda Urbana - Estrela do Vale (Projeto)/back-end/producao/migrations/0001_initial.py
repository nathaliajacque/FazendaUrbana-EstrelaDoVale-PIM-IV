# Generated by Django 5.1.1 on 2024-10-27 01:43

import django.db.models.deletion
from django.conf import settings
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('cliente', '0002_initial'),
        ('pedido', '0001_initial'),
        migrations.swappable_dependency(settings.AUTH_USER_MODEL),
    ]

    operations = [
        migrations.CreateModel(
            name='Producao',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('status', models.CharField(choices=[('EM_PLANEJAMENTO', 'Em planejamento'), ('EM_PRODUCAO', 'Em produção'), ('CONCLUIDO', 'Concluído'), ('CANCELADO', 'Cancelado')], default='Em planejamento', max_length=20)),
                ('prazo_entrega', models.DateField(blank=True, null=True)),
                ('data_inicio', models.DateField()),
                ('data_cadastro', models.DateTimeField(auto_now_add=True)),
                ('controle_ambiente', models.BooleanField(default=False)),
                ('cliente', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, to='cliente.cliente')),
                ('pedido', models.ForeignKey(on_delete=django.db.models.deletion.CASCADE, related_name='producao_pedido', to='pedido.pedido')),
                ('usuario', models.ForeignKey(editable=False, null=True, on_delete=django.db.models.deletion.SET_NULL, to=settings.AUTH_USER_MODEL)),
            ],
            options={
                'verbose_name': 'Produção',
                'verbose_name_plural': 'Produções',
            },
        ),
    ]
