from django.db import models
from funcionario.models import Funcionario
from django.contrib.auth.models import User
from django.core.validators import RegexValidator


class RelatorioFuncionario(models.Model):
    id_funcionario = models.AutoField(primary_key=True)
    nome = models.CharField(max_length=255)
    cargo = models.CharField(max_length=50)
    cpf = models.CharField(max_length=11)
    rg = models.CharField(max_length=10)
    orgao_emissor = models.CharField(max_length=10)
    contato = models.CharField(max_length=255)
    email = models.EmailField(max_length=255)
    usuario = models.ForeignKey(
        User, on_delete=models.SET_NULL, null=True, editable=False
    )
    data_admissao = models.DateField()
    data_cadastro = models.DateTimeField()
    logradouro = models.CharField(max_length=50)
    bairro = models.CharField(max_length=50)
    numero = models.CharField(max_length=5)
    cep = models.CharField(max_length=9)
    complemento = models.CharField(max_length=30, blank=True, null=True)
    cidade = models.CharField(max_length=30)
    uf = models.CharField(max_length=2)

    def __str__(self):
        return f"Relatório de {self.nome} - {self.data_geracao.strftime('%d/%m/%Y')}"

    @classmethod
    def gerar_relatorio(cls, id_funcionario):
        try:
            funcionario = Funcionario.objects.get(id_funcionario=id_funcionario)
            relatorio = cls(
                id_funcionario=funcionario.id_funcionario,
                nome=funcionario.nome,
                cargo=funcionario.cargo,
                cpf=funcionario.cpf,
                rg=funcionario.rg,
                orgao_emissor=funcionario.orgao_emissor,
                contato=funcionario.contato,
                email=funcionario.email,
                usuario=funcionario.usuario,
                data_admissao=funcionario.data_admissao,
                data_cadastro=funcionario.data_cadastro,
                logradouro=funcionario.logradouro,
                bairro=funcionario.bairro,
                numero=funcionario.numero,
                cep=funcionario.cep,
                complemento=funcionario.complemento,
                cidade=funcionario.cidade,
                uf=funcionario.uf,
            )
            relatorio.save()
            return relatorio
        except Funcionario.DoesNotExist:
            return None
