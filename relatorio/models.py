from django.db import models
from django.contrib.auth.models import User


class RelatorioFuncionario(models.Model):
    funcionario = models.OneToOneField(
        "funcionario.Funcionario", on_delete=models.CASCADE
    )
    data_relatorio = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"Relatório do funcionário: {self.funcionario.nome}"

    class Meta:
        verbose_name = "Relatório de Funcionário"
        verbose_name_plural = "Relatório de Funcionários"

    def obter_dados_funcionario(self):
        from funcionario.models import Funcionario

        """Retorna os dados completos do funcionário no relatório"""
        dados_funcionario = {
            "Nome": self.funcionario.nome,
            "Cargo": self.funcionario.cargo,
            "CPF": self.funcionario.cpf,
            "RG": self.funcionario.rg,
            "Órgão Emissor": self.funcionario.orgao_emissor,
            "Contato": self.funcionario.contato,
            "Email": self.funcionario.email,
            "Data de Admissão": self.funcionario.data_admissao,
            "Data de Cadastro": self.funcionario.data_cadastro,
            "Endereço": {
                "Logradouro": self.funcionario.logradouro,
                "Bairro": self.funcionario.bairro,
                "Número": self.funcionario.numero,
                "CEP": self.funcionario.cep,
                "Complemento": self.funcionario.complemento,
                "Cidade": self.funcionario.cidade,
                "Estado (UF)": self.funcionario.uf,
            },
            "Observação": self.funcionario.observacao,
        }
        return dados_funcionario

    def exportar_relatorio(self):
        """Exemplo simples de como exportar o relatório em formato de texto"""
        dados = self.obter_dados_funcionario()
        relatorio = f"Relatório do Funcionário: {dados['Nome']}\n"
        relatorio += f"Cargo: {dados['Cargo']}\n"
        relatorio += f"CPF: {dados['CPF']}\n"
        relatorio += f"RG: {dados['RG']} ({dados['Órgão Emissor']})\n"
        relatorio += f"Contato: {dados['Contato']}\n"
        relatorio += f"Email: {dados['Email']}\n"
        relatorio += f"Usuário: {dados['Usuário']}\n"
        relatorio += f"Data de Admissão: {dados['Data de Admissão']}\n"
        relatorio += f"Endereço: {dados['Endereço']['Logradouro']}, {dados['Endereço']['Número']}, {dados['Endereço']['Bairro']}, {dados['Endereço']['Cidade']}-{dados['Endereço']['Estado (UF)']}, CEP: {dados['Endereço']['CEP']}\n"
        relatorio += f"Observação: {dados['Observação']}\n"
        return relatorio
