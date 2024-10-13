from django.contrib import admin
from .models import Pedido
from .models import ItemPedido
from .models import Fornecedor


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1
    fields = (
        "produto",
        "quantidade",
        "fornecedor",
        "prazo_entrega",
    )
    readonly_fields = ("prazo_entrega", "fornecedor")


class PedidoAdmin(admin.ModelAdmin):
    inlines = [ItemPedidoInline]
    list_display = (
        "id",
        "status",
        "cliente",
        "data_venda",
        "total",
        "get_fornecedores",  # Adiciona o método para exibir fornecedores e prazo entrega
        "get_prazo_entrega",
        # "data_cadastro",
        # "usuario",
    )
    list_filter = ("status", "data_venda", "data_cadastro")
    search_fields = ("id", "cliente__nome_fantasia", "cliente__razao_social")
    readonly_fields = ("id", "usuario", "data_cadastro", "total")

    def get_fornecedores(self, obj):
        return ", ".join(set(item.fornecedor.nome_fantasia for item in obj.itens.all()))

    get_fornecedores.short_description = "Fornecedor"  # Título da coluna

    def get_prazo_entrega(self, obj):
        return ", ".join(
            set(item.prazo_entrega.strftime("%d/%m/%Y") for item in obj.itens.all())
        )

    get_prazo_entrega.short_description = "Prazo Entrega"  # Título da coluna


admin.site.register(Pedido, PedidoAdmin)
admin.site.register(ItemPedido)
