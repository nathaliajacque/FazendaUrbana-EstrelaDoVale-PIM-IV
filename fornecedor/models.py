from django.db import models
from cliente.models import Cliente


class Fornecedor(Cliente):
    id_fornecedor = models.AutoField(primary_key=True)
    prazo_entrega_dias = models.IntegerField()

    def __str__(self):
        return (
            f"{self.nome_fantasia} - Prazo de Entrega: {self.prazo_entrega_dias} dias"
        )

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
