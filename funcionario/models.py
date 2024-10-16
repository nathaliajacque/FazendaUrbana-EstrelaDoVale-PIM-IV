from django.db import models
from utils.validatorcpf import validate_cpf
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class Funcionario(models.Model):
    CARGO_CHOICES = sorted(
        [
            ("", "Selecione o cargo"),
            ("Gerente de Produção Agrícola", "Gerente de Produção Agrícola"),
            ("Vendas e Marketing", "Vendas e Marketing"),
            ("Analista de Recursos Humanos", "Analista de Recursos Humanos"),
            ("Auxiliar de Produção Agrícola", "Auxiliar de Produção Agrícola"),
            ("Auxiliar de Limpeza e Manutenção", "Auxiliar de Limpeza e Manutenção"),
            ("Assistente Administrativo", "Assistente Administrativo"),
            ("Analista de Sustentabilidade", "Analista de Sustentabilidade"),
            ("Técnico em Meio Ambiente", "Técnico em Meio Ambiente"),
            ("Engenheiro Agrônomo", "Engenheiro Agrônomo"),
            ("Agrônomo", "Agrônomo"),
            ("Técnico em Agricultura", "Técnico em Agricultura"),
            ("Especialista em Hidroponia", "Especialista em Hidroponia"),
        ],
        key=lambda x: x[0],
    )

    UF_CHOICES = [
        ("", "Selecione o estado"),
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

    ORGAO_CHOICES = [
        ("", "Selecione o órgão emissor"),
        ("SSP/AC", "SSP/AC"),
        ("SSP/AL", "SSP/AL"),
        ("SSP/AP", "SSP/AP"),
        ("SSP/AM", "SSP/AM"),
        ("SSP/BA", "SSP/BA"),
        ("SSPDS/CE", "SSPDS/CE"),
        ("SSP/DF", "SSP/DF"),
        ("SESP/ES", "SESP/ES"),
        ("SSP/GO", "SSP/GO"),
        ("SSP/MA", "SSP/MA"),
        ("SSP/MT", "SSP/MT"),
        ("SSP/MS", "SSP/MS"),
        ("SSP/MG", "SSP/MG"),
        ("SSP/PA", "SSP/PA"),
        ("SSP/PB", "SSP/PB"),
        ("SSP/PR", "SSP/PR"),
        ("SSP/PE", "SSP/PE"),
        ("SSP/PI", "SSP/PI"),
        ("SSP/RJ", "SSP/RJ"),
        ("SESED/RN", "SESED/RN"),
        ("SSP/RS", "SSP/RS"),
        ("SESDEC/RO", "SESDEC/RO"),
        ("SESP/RR", "SESP/RR"),
        ("SSP/SC", "SSP/SC"),
        ("SSP/SP", "SSP/SP"),
        ("SSP/SE", "SSP/SE"),
        ("SSP/TO", "SSP/TO"),
    ]

    nome = models.CharField(max_length=255)
    cargo = models.CharField(max_length=50, choices=CARGO_CHOICES)
    cpf = models.CharField(max_length=11, unique=True, validators=[validate_cpf])
    rg = models.CharField(max_length=10)
    orgao_emissor = models.CharField(
        max_length=10, choices=ORGAO_CHOICES, default="SSP"
    )
    contato = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, editable=False
    )
    data_admissao = models.DateField()
    data_cadastro = models.DateTimeField(auto_now_add=True, editable=False)

    cep_validator = RegexValidator(
        regex=r"^\d{5}-\d{3}$", message="CEP deve estar no formato XXXXX-XXX"
    )

    # Atributos do endereço diretamente na classe Cliente
    logradouro = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50)
    numero = models.CharField(max_length=5)
    cep = models.CharField(max_length=9, validators=[cep_validator])
    complemento = models.CharField(max_length=30, blank=True, null=True)
    cidade = models.CharField(max_length=30)
    uf = models.CharField(
        max_length=2,
        blank=True,
        choices=(UF_CHOICES),
    )
    observacao = models.TextField(max_length=255, blank=True)

    def __str__(self):
        return self.nome + " - " + self.cargo

    class Meta:
        verbose_name = "Funcionário"
        verbose_name_plural = "Funcionários"
