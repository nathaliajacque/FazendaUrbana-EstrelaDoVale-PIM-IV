from django.db import models
from usuario.models import Usuario
from utils.statusmodel import StatusModel
from utils.validatorcnpj import validate_cnpj
from django.core.validators import RegexValidator


class Fornecedor(StatusModel):
    UF_CHOICES = [
        ("AC", "Acre"),
        ("AL", "Alagoas"),
        ("AP", "Amapá"),
        ("AM", "Amazonas"),
        ("BA", "Bahia"),
        ("CE", "Ceará"),
        ("DF", "Distrito Federal"),
        ("ES", "Espírito Santo"),
        ("GO", "Goiás"),
        ("MA", "Maranhão"),
        ("MT", "Mato Grosso"),
        ("MS", "Mato Grosso do Sul"),
        ("MG", "Minas Gerais"),
        ("PA", "Pará"),
        ("PB", "Paraíba"),
        ("PR", "Paraná"),
        ("PE", "Pernambuco"),
        ("PI", "Piauí"),
        ("RJ", "Rio de Janeiro"),
        ("RN", "Rio Grande do Norte"),
        ("RS", "Rio Grande do Sul"),
        ("RO", "Rondônia"),
        ("RR", "Roraima"),
        ("SC", "Santa Catarina"),
        ("SP", "São Paulo"),
        ("SE", "Sergipe"),
        ("TO", "Tocantins"),
    ]
    prazo_entrega_dias = models.IntegerField()
    data_cadastro = models.DateTimeField(auto_now_add=True, editable=False)
    nome_fantasia = models.CharField(max_length=255)
    razao_social = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=14, unique=True, validators=[validate_cnpj])
    ie = models.CharField(max_length=20, blank=True, null=True)
    im = models.CharField(max_length=20, blank=True, null=True)
    contato = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    email = models.EmailField(max_length=255, blank=True, null=True)
    usuario = models.ForeignKey(
        Usuario, on_delete=models.SET_NULL, null=True, editable=False
    )
    cep_validator = RegexValidator(
        regex=r"^\d{5}-\d{3}$", message="CEP deve estar no formato XXXXX-XXX"
    )
    logradouro = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50)
    numero = models.CharField(max_length=5)
    cep = models.CharField(max_length=9, validators=[cep_validator])
    complemento = models.CharField(max_length=30, blank=True, null=True)
    cidade = models.CharField(max_length=30)
    uf = models.CharField(
        max_length=2,
        default="SP",
        choices=UF_CHOICES,
    )
    observacao = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return (
            f"{self.nome_fantasia} - Prazo de Entrega: {self.prazo_entrega_dias} dias"
        )

    class Meta:
        verbose_name = "Fornecedor"
        verbose_name_plural = "Fornecedores"
