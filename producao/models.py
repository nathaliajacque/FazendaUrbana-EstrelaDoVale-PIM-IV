from django.db import models
from django.core.exceptions import ValidationError
from django.contrib.auth.models import User
from cliente.models import Cliente
from pedido.models import Pedido


# Ver aula 567. Projeto e-commerce - Criando os models Produto e Variação, usar variação para associar o pedido
# a produção, talvez
class Producao(models.Model):
    STATUS_CHOICES = [
        ("Em planejamento", "Em planejamento"),
        ("Em produção", "Em produção"),
        ("Concluído", "Concluído"),
        ("Cancelado", "Cancelado"),
    ]

    id_producao = models.AutoField(primary_key=True)
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name="producoes"
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Em planejamento"
    )
    data_inicio = models.DateField()
    data_cadastro = models.DateTimeField(auto_now_add=True, editable=False)
    prazo_entrega = models.DateField()
    controle_ambiente = models.BooleanField(default=False)
    usuario = models.ForeignKey(User, on_delete=models.SET_NULL, null=True)

    def clean(self):
        if self.status == "Em planejamento" and not self.controle_ambiente:
            raise ValidationError(
                "Controle de ambiente deve ser marcado quando o status é 'Em planejamento'."
            )

    def produtos_do_pedido(self):
        return self.pedido.produto.all()  # relação ManyToMany em Pedido

    def get_codigo_pedido(self):
        return self.pedido.id_pedido if self.pedido else None

    def get_prazo_entrega(self):
        return self.pedido.prazo_entrega if self.pedido else None

    def get_produtos(self):
        return self.pedido.itens.all() if self.pedido else None

    def get_clientes(self):
        return self.pedido.cliente.all() if self.pedido else None

    def __str__(self):
        return f"Produção n° {self.id_producao} - Pedido n° {self.get_codigo_pedido()}"

    class Meta:
        verbose_name = "Produção"
        verbose_name_plural = "Produções"
