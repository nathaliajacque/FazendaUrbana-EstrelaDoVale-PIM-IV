from django.contrib import admin
from .models import RelatorioFuncionario


class RelatorioFuncionarioAdmin(admin.ModelAdmin):
    list_display = (
        "funcionario",
        "data_relatorio",
        "obter_nome",
        "obter_cargo",
        "obter_cpf",
        "obter_rg",
        "obter_orgao_emissor",
        "obter_contato",
        "obter_email",
        "obter_usuario",
        "obter_data_admissao",
        "obter_logradouro",
        "obter_bairro",
        "obter_numero",
        "obter_cep",
        "obter_complemento",
        "obter_cidade",
        "obter_uf",
        "obter_data_cadastro",
    )
    list_filter = (
        "data_relatorio",
        "funcionario__cargo",
        "funcionario__uf",
    )
    search_fields = (
        "funcionario__nome",
        "funcionario__cpf",
        "funcionario__rg",
        "funcionario__email",
        "funcionario__contato",
    )
    readonly_fields = ("data_relatorio",)

    def obter_nome(self, obj):
        return obj.funcionario.nome

    obter_nome.short_description = "Nome"

    def obter_cargo(self, obj):
        return obj.funcionario.cargo

    obter_cargo.short_description = "Cargo"

    def obter_cpf(self, obj):
        return obj.funcionario.cpf

    obter_cpf.short_description = "CPF"

    def obter_rg(self, obj):
        return obj.funcionario.rg

    obter_rg.short_description = "RG"

    def obter_orgao_emissor(self, obj):
        return obj.funcionario.orgao_emissor

    obter_orgao_emissor.short_description = "Órgão Emissor"

    def obter_contato(self, obj):
        return obj.funcionario.contato

    obter_contato.short_description = "Contato"

    def obter_email(self, obj):
        return obj.funcionario.email

    obter_email.short_description = "Email"

    def obter_usuario(self, obj):
        return obj.funcionario.usuario.username if obj.funcionario.usuario else "N/A"

    obter_usuario.short_description = "Usuário"

    def obter_data_admissao(self, obj):
        return obj.funcionario.data_admissao

    obter_data_admissao.short_description = "Data de Admissão"

    def obter_data_cadastro(self, obj):
        return obj.funcionario.data_cadastro

    obter_data_cadastro.short_description = "Data de Cadastro"

    def obter_logradouro(self, obj):
        return obj.funcionario.logradouro

    obter_logradouro.short_description = "Logradouro"

    def obter_bairro(self, obj):
        return obj.funcionario.bairro

    obter_bairro.short_description = "Bairro"

    def obter_numero(self, obj):
        return obj.funcionario.numero

    obter_numero.short_description = "Número"

    def obter_cep(self, obj):
        return obj.funcionario.cep

    obter_cep.short_description = "CEP"

    def obter_complemento(self, obj):
        return obj.funcionario.complemento

    obter_complemento.short_description = "Complemento"

    def obter_cidade(self, obj):
        return obj.funcionario.cidade

    obter_cidade.short_description = "Cidade"

    def obter_uf(self, obj):
        return obj.funcionario.uf

    obter_uf.short_description = "UF"


admin.site.register(RelatorioFuncionario, RelatorioFuncionarioAdmin)
