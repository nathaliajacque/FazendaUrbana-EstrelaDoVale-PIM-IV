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
from django.utils import timezone
import os
from django.contrib.auth.models import User
from utils.statusmodel import StatusModel


class Produto(StatusModel):
    CATEGORIA_CHOICES = [
        ("Hortaliça de Flor", "Hortaliça de Flor"),
        ("Hortaliça de Folha", "Hortaliça de Folha"),
        ("Tubérculo", "Tubérculo"),
    ]

    # TODO: Inserir fornecedor
    id_produto = models.AutoField(primary_key=True)
    descricao = models.CharField(max_length=255)
    categoria = models.CharField(max_length=255, choices=CATEGORIA_CHOICES)
    fornecedor = models.CharField(max_length=255)
    grupo = models.CharField(max_length=255)
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
            return {
                "id_produto": produto.id_produto,
                "status": produto.status,
                "fornecedor": produto.fornecedor,
                "usuario": produto.usuario.username,
                "data_cadastro": produto.data_cadastro,
                "descricao": produto.descricao,
                "categoria": produto.categoria,
                "grupo": produto.grupo,
                "temperatura": produto.temperatura,
                "umidade": produto.umidade,
                "iluminacao": produto.iluminacao,
                "intensidade_led": produto.intensidade_led,
                "nivel_agua": produto.nivel_agua,
                "crescimento": produto.crescimento,
                "solucao_nutritiva": produto.solucao_nutritiva,
                "observacao": produto.observacao,
            }
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

    def __self__(self):
        return self.descricao

    class Meta:
        verbose_name = "Produto"
        verbose_name_plural = "Produtos"


# parei no 38:25 / 43:46, terminar de fazer o CRUD de produto
