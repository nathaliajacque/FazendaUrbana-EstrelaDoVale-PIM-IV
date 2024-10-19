from django.db import models
from django.core.exceptions import ValidationError
from usuario.models import Usuario
from cliente.models import Cliente
from pedido.models import Pedido


class Producao(models.Model):
    STATUS_CHOICES = [
        ("EM_PLANEJAMENTO", "Em planejamento"),
        ("EM_PRODUCAO", "Em produção"),
        ("CONCLUIDO", "Concluído"),
        ("CANCELADO", "Cancelado"),
    ]
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name="producoes"
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE)
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Em planejamento"
    )
    prazo_entrega = models.DateField(null=True, blank=True)
    data_inicio = models.DateField()
    data_cadastro = models.DateTimeField(auto_now_add=True, editable=False)
    controle_ambiente = models.BooleanField(default=False)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, editable=False
    )

    def clean(self):
        if self.status == "Em planejamento" and not self.controle_ambiente:
            raise ValidationError(
                "Controle de ambiente deve ser marcado quando o status é 'Em planejamento'."
            )

    def produtos_do_pedido(self):
        return self.pedido.produto.all()  # relação ManyToMany em Pedido

    def get_codigo_pedido(self):
        return self.pedido.id if self.pedido else None

    def get_prazo_entrega(self):
        return self.pedido.prazo_entrega if self.pedido else None

    def get_clientes(self):
        return self.pedido.cliente.all() if self.pedido else None

    # def get_produtos(self):
    #    return self.pedido.itens.all() if self.pedido else None

    def __str__(self):
        return f"Produção n° {self.id} - Pedido n° {self.get_codigo_pedido()}"

    class Meta:
        verbose_name = "Produção"
        verbose_name_plural = "Produções"
