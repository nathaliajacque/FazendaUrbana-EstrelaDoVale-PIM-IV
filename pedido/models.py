from django.db import models
from usuario.models import Usuario
from cliente.models import Cliente
from produto.models import Produto
from fornecedor.models import Fornecedor
from datetime import timedelta
from django.core.mail import send_mail
from django.template.loader import render_to_string
from django.conf import settings


class Pedido(models.Model):
    STATUS_CHOICES = [
        ("EM_ANDAMENTO", "Em andamento"),
        ("CONCLUIDO", "Concluído"),
        ("CANCELADO", "Cancelado"),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Em andamento"
    )

    total = models.FloatField(default=0)
    data_venda = models.DateField()
    data_cadastro = models.DateTimeField(auto_now_add=True, editable=False)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, editable=False
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True)

    @classmethod
    def cancelar_pedido_venda(self):
        self.status = "Cancelado"
        self.save()

    # Método para recalcular o total do pedido com base nas quantidades dos itens
    def calcular_total(self):
        total_quantidade = sum(item.quantidade for item in self.itens.all())
        self.total = total_quantidade
        self.save()

    def calcular_prazo_entrega(self):
        for item in self.itens.all():  # Itera sobre os itens do pedido
            # Calcula o prazo de entrega para cada item do pedido
            prazo_entrega_dias = (
                item.produto.calcular_prazo_entrega()
            )  # Método no Produto
            item.prazo_entrega = self.data_venda + timedelta(
                days=prazo_entrega_dias
            )  # Atualiza o prazo do item
            item.save()  # Salva o item do pedido com o novo prazo de entrega
            self.save()  # Salva o pedido após atualizar os itens

    # TODO: Arrumar o método para enviar e-mail ao fornecedor, deve enviar quando for cancelado também

    def save(self, *args, **kwargs):
        is_new = not self.pk
        status_anterior = None

        if not is_new:
            status_anterior = Pedido.objects.get(pk=self.pk).status

        super().save(*args, **kwargs)

        if (is_new and self.status == "CONCLUIDO") or (
            status_anterior != self.status and self.status == "CONCLUIDO"
        ):
            self.enviar_email_conclusao()

        if status_anterior != self.status and self.status == "CANCELADO":
            self.enviar_email_cancelamento()

    def enviar_email_conclusao(self):
        itens = []
        fornecedor = None
        for item in self.itens.all():
            produto = item.produto
            fornecedor = produto.fornecedor
            itens.append(
                {
                    "produto": produto.descricao,
                    "quantidade": item.quantidade,
                }
            )

        if fornecedor:
            subject = "Estrela do Vale - Solicitação de insumos"
            message = render_to_string(
                "email_template.html",
                {
                    "fornecedor": fornecedor,
                    "itens": itens,
                    "data_venda": self.data_venda,
                    "pedido_id": self.id,
                },
            )
            recipient_list = [fornecedor.email]

            send_mail(
                subject,
                "",
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                html_message=message,
                fail_silently=False,
            )

    def enviar_email_cancelamento(self):
        itens = []
        fornecedor = None
        for item in self.itens.all():
            produto = item.produto
            fornecedor = produto.fornecedor
            itens.append(
                {
                    "produto": produto.descricao,
                    "quantidade": item.quantidade,
                }
            )

        if fornecedor:
            subject = "Estrela do Vale - Cancelamento de pedido"
            message = render_to_string(
                "email_template_cancelamento.html",
                {
                    "fornecedor": fornecedor,
                    # "pedido_id": self.id,
                    "itens": itens,
                    "data_venda": self.data_venda,
                    "pedido_id": self.id,
                },
            )
            recipient_list = [fornecedor.email]

            send_mail(
                subject,
                "",
                settings.DEFAULT_FROM_EMAIL,
                recipient_list,
                html_message=message,
                fail_silently=False,
            )

    def __str__(self):
        return f"Pedido n° {self.id} - {self.cliente.nome_fantasia}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedido"


class ItemPedido(models.Model):
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, related_name="itens_pedido"
    )
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, editable=False)
    pedido = models.ForeignKey(
        Pedido, on_delete=models.CASCADE, related_name="itens"
    )  # Relacionamento com Pedido
    producao = models.ForeignKey(
        "producao.Producao", on_delete=models.CASCADE, null=True, blank=True
    )
    quantidade = models.PositiveIntegerField()
    descricao = models.CharField(max_length=255, editable=False)
    prazo_entrega = models.DateField(editable=False)

    def calcular_prazo_entrega(self):
        fornecedor = self.produto.fornecedor
        prazo_entrega_dias = self.produto.crescimento + fornecedor.prazo_entrega_dias
        self.prazo_entrega = self.pedido.data_venda + timedelta(days=prazo_entrega_dias)

    def save(self, *args, **kwargs):
        self.fornecedor = self.produto.fornecedor
        self.descricao = self.produto.descricao
        self.calcular_prazo_entrega()
        super().save(*args, **kwargs)
        self.pedido.calcular_total()

    def __str__(self):
        return f"{self.produto.descricao} - {self.quantidade} unidade(s)"

    class Meta:
        verbose_name = "Item do Pedido"
        verbose_name_plural = "Itens do Pedido"
