"""
Campos da Classe Pedido:

id_pedido: Chave primária para identificar o pedido de venda.
id_pedido: Número do pedido.
status: Campo de escolha para o status do pedido.
data_venda: Data da venda.
data_cadastro: Data de cadastro do pedido (preenchida automaticamente).
usuario: Chave estrangeira para o usuário que criou o pedido.
cliente: Chave estrangeira para o cliente associado ao pedido.
prazo_entrega: Prazo de entrega do pedido.
Métodos da Classe Pedido:

create_pedido_venda: Método de classe para criar um novo pedido de venda.
get_pedido_venda: Método de classe para obter um pedido de venda pelo ID.
update_pedido_venda: Método de classe para atualizar um pedido de venda.
concluir_pedido_venda: Método de instância para concluir um pedido de venda.
validar_dados: Método de instância para validar os dados do pedido.
cancelar_pedido_venda: Método de instância para cancelar um pedido de venda.
"""

from django.db import models
from django.contrib.auth.models import User
from cliente.models import Cliente
from produto.models import Produto
from fornecedor.models import Fornecedor
from datetime import timedelta

# TODO: Fazer com que o pedido gere um prazo de acordo com o tempo de entrega do fornecedor + dias
# do crescimento do insumo


class Pedido(models.Model):
    STATUS_CHOICES = [
        ("Em andamento", "Em andamento"),
        ("Concluído", "Concluído"),
        ("Cancelado", "Cancelado"),
    ]
    status = models.CharField(
        max_length=20, choices=STATUS_CHOICES, default="Em andamento"
    )
    # adicionado total
    total = models.FloatField(default=0)
    data_venda = models.DateField()
    data_cadastro = models.DateTimeField(auto_now_add=True, editable=False)
    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, editable=False
    )
    cliente = models.ForeignKey(Cliente, on_delete=models.CASCADE, blank=True)

    def __str__(self):
        return f"Pedido n° {self.id_pedido} - {self.cliente.nome_fantasia}"

    @classmethod
    def create_pedido(cls, **kwargs):
        pedido = cls(**kwargs)
        pedido.save()
        return pedido

    @classmethod
    def get_pedido(cls, id_pedido):
        try:
            pedido = cls.objects.get(id_pedido=id_pedido)
            return pedido
        except cls.DoesNotExist:
            return None

    @classmethod
    def update_pedido(cls, id_pedido, **kwargs):
        try:
            pedido = cls.objects.get(id_pedido=id_pedido)
            for key, value in kwargs.items():
                setattr(pedido, key, value)
            pedido.save()
            return pedido
        except cls.DoesNotExist:
            return None

    def cancelar_pedido_venda(self):
        self.status = "Cancelado"
        self.save()

    # def concluir_pedido_venda(self):
    #     self.status = "Em andamento"
    #     self.save()

    # def concluir_pedido_venda(self):
    #     self.status = "Concluído"
    #     self.save()

    # REMOVIDO
    # def calcular_prazo_entrega(self):
    #   self.prazo_entrega = self.produto.calcular_prazo_entrega()
    #   self.save()

    def calcular_data_entrega(self):
        produto = Produto.objects.get(id=self.produto_id)
        prazo_entrega_dias = produto.calcular_prazo_entrega()
        self.prazo_entrega = self.data_venda + timedelta(days=prazo_entrega_dias)
        self.save()

    # Método para recalcular o total do pedido com base nas quantidades dos itens
    def calcular_total(self):
        total_quantidade = sum(item.quantidade for item in self.itens.all())
        self.total = total_quantidade
        self.save()

    @property
    def prazo_entrega_data(self):
        # Calcula a data de entrega com base nos itens do pedido
        prazo_entrega_dias = 0
        for item in self.itens.all():
            fornecedor = (
                item.produto.fornecedor
            )  # Supondo que Produto tem um campo fornecedor
            prazo_entrega_dias += (
                item.produto.tempo_crescimento + fornecedor.prazo_entrega_dias
            )
        return self.data_pedido + timedelta(days=prazo_entrega_dias)

    def validar_dados(self):
        # Adicione a lógica de validação aqui
        pass

    def __str__(self):
        return f"Pedido n° {self.id_pedido} - {self.cliente.nome_fantasia}"

    class Meta:
        verbose_name = "Pedido"
        verbose_name_plural = "Pedidos"


class ItemPedido(models.Model):
    produto = models.ForeignKey(
        Produto, on_delete=models.CASCADE, related_name="itens_pedido"
    )
    fornecedor = models.ForeignKey(Fornecedor, on_delete=models.CASCADE, editable=False)
    pedido = models.ForeignKey(Pedido, on_delete=models.CASCADE, related_name="itens")
    producao = models.ForeignKey(
        "producao.Producao", on_delete=models.CASCADE, null=True, blank=True
    )
    quantidade = models.PositiveIntegerField()
    descricao = models.CharField(max_length=255, editable=False)
    prazo_entrega = models.DateField(editable=False)

    def save(self, *args, **kwargs):
        # Salvar o pedido antes de calcular o prazo de entrega
        if not self.pedido.pk:
            self.pedido.save()
        self.fornecedor = self.produto.fornecedor
        self.descricao = self.produto.descricao
        fornecedor = (
            self.produto.fornecedor
        )  # Supondo que Produto tem um campo fornecedor
        prazo_entrega_dias = self.produto.crescimento + fornecedor.prazo_entrega_dias
        # Use o campo correto para data do pedido, provavelmente `data_venda`
        self.prazo_entrega = self.pedido.data_venda + timedelta(days=prazo_entrega_dias)
        super().save(*args, **kwargs)
        self.pedido.calcular_total()  # Atualizar o pedido para recalcular o total

    @classmethod
    def create_item(cls, produto, pedido, quantidade):
        item = cls(produto=produto, pedido=pedido, quantidade=quantidade)
        item.save()
        return item

    @classmethod
    def get_item(cls, id_item):
        try:
            item = cls.objects.get(id=id_item)
            return item
        except cls.DoesNotExist:
            return None

    @classmethod
    def update_item(cls, id_item, **kwargs):
        try:
            item = cls.objects.get(id=id_item)
            for key, value in kwargs.items():
                setattr(item, key, value)
            item.save()
            return item
        except cls.DoesNotExist:
            return None

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

    def calcular_valor_total(self):
        self.valor_total = self.quantidade * self.valor_unitario
        self.save()

    def __str__(self):
        return f"{self.produto.descricao} - {self.quantidade} unidade(s)"

    class Meta:
        verbose_name = "Item do pedido"
        verbose_name_plural = "Itens do pedido"
