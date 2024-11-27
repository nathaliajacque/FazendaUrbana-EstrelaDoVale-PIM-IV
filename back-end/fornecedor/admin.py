from django.contrib import admin
from .models import Fornecedor


class FornecedorAdmin(admin.ModelAdmin):
    list_display = (
        "id",
        "status",
        "nome_fantasia",
        "razao_social",
        "cnpj",
        "contato",
        "prazo_entrega_dias",
        "data_cadastro",
    )
    search_fields = (
        "id",
        "nome_fantasia",
        "razao_social",
        "cnpj",
        "contato",
        "id",
    )
    list_filter = ("prazo_entrega_dias", "cidade", "uf")
    readonly_fields = ("data_cadastro", "usuario", "id")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Fornecedor, FornecedorAdmin)
