from django.contrib import admin
from .models import Produto  # Importando a classe Produto diretamente do módulo models


class ProdutoAdmin(admin.ModelAdmin):
    list_display = (
        "id_produto",
        "status",
        "descricao",
        "categoria",
        "observacao",
        "data_cadastro",
    )
    readonly_fields = ("usuario", "data_cadastro", "id_produto")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Produto, ProdutoAdmin)
