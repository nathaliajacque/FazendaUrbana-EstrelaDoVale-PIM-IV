from django.contrib import admin
from .models import Fornecedor


class FornecedorAdmin(admin.ModelAdmin):
    list_display = ("nome_fantasia", "razao_social", "cnpj", "prazo_entrega_dias")
    search_fields = ("nome_fantasia", "razao_social", "cnpj")
    list_filter = ("prazo_entrega_dias", "cidade", "uf")
    readonly_fields = ("data_cadastro", "usuario", "id_fornecedor")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Fornecedor, FornecedorAdmin)
