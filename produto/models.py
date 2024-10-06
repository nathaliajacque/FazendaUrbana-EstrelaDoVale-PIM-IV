"""
create_produto: Cria um novo produto com os atributos fornecidos e salva no banco de dados.
get_produto: Retorna um dicionário com os atributos do produto especificado pelo id_produto.
update_produto: Atualiza os atributos do produto especificado pelo id_produto com os valores fornecidos.
delete_produto: Exclui o produto especificado pelo id_produto.
inativar_produto: Define o status do produto especificado pelo id_produto como "Inativo".
ativar_produto: Define o status do produto especificado pelo id_produto como "Ativo".
CATEGORIA_CHOICES: Uma lista de tuplas onde cada tupla contém duas strings. A primeira string é o valor armazenado no banco de dados e a segunda string é a opção legível que será exibida nos formulários.
"""

from django.db import models
from django.contrib.auth.models import User
from utils.statusmodel import StatusModel
from fornecedor.models import Fornecedor


class Produto(StatusModel):
    CATEGORIA_CHOICES = [
        ("", "Selecione a categoria"),
        ("Hortaliça de Flor", "Hortaliça de Flor"),
        ("Hortaliça de Folha", "Hortaliça de Folha"),
        ("Tubérculo", "Tubérculo"),
    ]

    # TODO: Inserir fornecedor
    id_produto = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255)
    categoria = models.CharField(max_length=255, choices=CATEGORIA_CHOICES)
    fornecedor = models.ForeignKey(Fornecedor, models.CASCADE, null=True, blank=True)
    grupo = models.CharField(max_length=255, blank=True)
    temperatura = models.FloatField()
    umidade = models.FloatField()
    iluminacao = models.FloatField()
    crescimento = models.FloatField()
    intensidade_led = models.FloatField()
    nivel_agua = models.FloatField()
    solucao_nutritiva = models.TextField(max_length=255)
    observacao = models.TextField(max_length=255, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, editable=False)
    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, editable=False
    )

    @classmethod
    def create_produto(cls, **kwargs):
        produto = cls(**kwargs)
        produto.save()
        return produto

    @classmethod
    def get_produto(cls, id_produto):
        try:
            produto = cls.objects.get(id_produto=id_produto)
            return produto
        except cls.DoesNotExist:
            return None

    @classmethod
    def update_produto(cls, id_produto, **kwargs):
        try:
            produto = cls.objects.get(id_produto=id_produto)
            for key, value in kwargs.items():
                if key != "usuario":  # Impede a alteração do usuário
                    setattr(produto, key, value)
            produto.save()
            return produto
        except cls.DoesNotExist:
            return None

    def calcular_prazo_entrega(self):
        return self.fornecedor.prazo_entrega_dias + self.crescimento

    def __str__(self):
        return f"{self.descricao}"

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"
