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

    # TODO: Verificar logica do pedido, caso tenha iniciado a produção. Caso cancelado o pedido de venda, deve ser cancelado o pedido de produção
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
        if self.pk:  # Verifica se o objeto já existe (ou seja, não é um novo pedido)
            status_anterior = Pedido.objects.get(pk=self.pk).status
        else:
            status_anterior = None

        super().save(*args, **kwargs)  # Salva o objeto Pedido primeiro

        # Verifica se o status é "CONCLUIDO" antes de salvar
        if status_anterior != self.status == "CONCLUIDO":

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
                subject = "Solicitação de insumos"
                message = render_to_string(
                    "email_template.html",
                    {
                        "fornecedor": fornecedor,
                        "itens": itens,
                        "data_venda": self.data_venda,
                    },
                )
                recipient_list = [fornecedor.email]  # Campo de email do fornecedor

                # Envia o e-mail
                send_mail(
                    subject,
                    "",  # Corpo do email em texto simples
                    settings.DEFAULT_FROM_EMAIL,
                    recipient_list,
                    html_message=message,  # Corpo do e-mail em HTML
                    fail_silently=False,
                )

    def __str__(self):
        return f"Pedido n° {self.id} - {self.cliente.nome_fantasia}"


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

    @classmethod
    def create_item(cls, produto, pedido, quantidade, producao_instance=None):
        item = cls(produto=produto, pedido=pedido, quantidade=quantidade)
        item.fornecedor = produto.fornecedor  # Garante que o fornecedor seja setado
        item.descricao = produto.descricao  # Garante que a descrição seja setada

        if producao_instance:  # Verifica se a produção foi fornecida
            item.producao = producao_instance  # Atribui a produção ao item

        item.save()  # Salva o item no banco de dados
        return item

    @classmethod
    def get_item(cls, id_item):
        try:
            item = cls.objects.get(id=id_item)
            return item
        except cls.DoesNotExist:
            return None

    def update_item(cls, id_item, **kwargs):
        try:
            item = cls.objects.get(id=id_item)
            for key, value in kwargs.items():
                setattr(item, key, value)
            item.save()
            return item
        except cls.DoesNotExist:
            return None

    @classmethod
    def remove_item(cls, item_id, pedido):
        try:
            item = cls.objects.get(id=item_id, pedido=pedido)
            item.delete()
            # Recalcular o total do pedido após remover o item
            pedido.calcular_total()
            return True
        except cls.DoesNotExist:
            return False

    @classmethod
    def list_items(cls, pedido):
        return cls.objects.filter(pedido=pedido)

    def __str__(self):
        return f"{self.produto.descricao} - {self.quantidade} unidade(s)"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"
