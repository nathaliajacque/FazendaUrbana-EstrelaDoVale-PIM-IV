from django.contrib import admin
from .models import Produto  # Importando a classe Produto diretamente do módulo models


class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        "id_produto",
        "status",
        "fornecedor",
        "descricao",
        "categoria",
        "fornecedor",
        "grupo",
        "temperatura",
        "umidade",
        "iluminacao",
        "crescimento",
        "intensidade_led",
        "nivel_agua",
        "solucao_nutritiva",
        "observacao",
        "data_cadastro",
        "usuario",
    )
    readonly_fields = ("usuario", "data_cadastro", "id_produto")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Produto, ProdutoAdmin)
