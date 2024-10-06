from django.contrib import admin
from .models import RelatorioFuncionario


class RelatorioFuncionarioAdmin(admin.ModelAdmin):
    list_display = (
        "id_funcionario",
        "nome",
        "cargo",
        "cpf",
        "rg",
        "orgao_emissor",
        "contato",
        "email",
        "usuario",
        "data_admissao",
        "data_cadastro",
        "logradouro",
        "bairro",
        "numero",
        "cep",
        "complemento",
        "cidade",
        "uf",
    )
    list_filter = ("cargo", "uf")
    search_fields = ("nome", "cpf", "rg", "email", "contato")


admin.site.register(RelatorioFuncionario, RelatorioFuncionarioAdmin)
