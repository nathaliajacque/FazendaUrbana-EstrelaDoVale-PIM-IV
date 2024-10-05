from django.db import models
from utils.validatorcpf import validate_cpf
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Funcionario(models.Model):
    id_funcionario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    cargo = models.CharField(max_length=255)
    cpf = models.CharField(max_length=18, unique=True, validators=[validate_cpf])
    rg = models.CharField(max_length=20)
    orgao = models.CharField(max_length=10)
    contato = models.CharField(max_length=255)
    email_1 = models.EmailField(max_length=255)
    email_2 = models.EmailField(max_length=255, blank=True, null=True)
    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, editable=False
    )
    data_cadastro = models.DateTimeField(auto_now_add=True, editable=False)

    cep_validator = RegexValidator(
        regex=r"^\d{5}-\d{3}$", message="CEP deve estar no formato XXXXX-XXX"
    )

    # Atributos do endereço diretamente na classe Cliente
    logradouro = models.CharField(max_length=255)
    bairro = models.CharField(max_length=255)
    numero = models.CharField(max_length=10)
    cep = models.CharField(max_length=9, validators=[cep_validator])
    complemento = models.CharField(max_length=255, blank=True, null=True)
    cidade = models.CharField(max_length=255)
    uf = models.CharField(
        max_length=2,
        default="SP",
        choices=(
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
        ),
    )

    def __str__(self):
        return self.nome
