from django.db import models
from django.contrib.auth.models import User
from utils.statusmodel import StatusModel
from utils.validatorcnpj import validate_cnpj
from django.core.validators import RegexValidator

# Remova a importação da classe Endereco
# from cliente.models import Endereco


class Cliente(StatusModel):
    id_cliente = models.AutoField(primary_key=True)
    data_cadastro = models.DateTimeField(auto_now_add=True, editable=False)
    nome_fantasia = models.CharField(max_length=255)
    razao_social = models.CharField(max_length=255)
    cnpj = models.CharField(max_length=18, unique=True, validators=[validate_cnpj])
    ie = models.CharField(max_length=20, blank=True, null=True)
    im = models.CharField(max_length=20, blank=True, null=True)
    contato = models.CharField(max_length=255)
    email_1 = models.EmailField(max_length=255)
    email_2 = models.EmailField(max_length=255, blank=True, null=True)
    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, editable=False
    )

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
    uf = models.CharField(max_length=2)

    def __str__(self):
        return self.nome_fantasia

    @classmethod
    def create_cliente(cls, **kwargs):
        cliente = cls(**kwargs)
        cliente.save()
        return cliente

    @classmethod
    def get_cliente(cls, id_cliente):
        try:
            cliente = cls.objects.get(id_cliente=id_cliente)
            return cliente
        except cls.DoesNotExist:
            return None

    @classmethod
    def atualizar_cliente(cls, id_cliente, **kwargs):
        try:
            cliente = cls.objects.get(id_cliente=id_cliente)
            for key, value in kwargs.items():
                setattr(cliente, key, value)
            cliente.save()
            return cliente
        except cls.DoesNotExist:
            return None

    def validar_dados(self):
        # Adicione a lógica de validação aqui
        pass

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"
