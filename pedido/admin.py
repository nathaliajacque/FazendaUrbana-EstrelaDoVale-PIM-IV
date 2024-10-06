from django.contrib import admin
from .models import PedidoVenda
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


class PedidoVendaAdmin(admin.ModelAdmin):
    inlines = [ItemPedidoInline]
    list_display = (
        "num_pedido",
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
    search_fields = ("num_pedido", "cliente__nome_fantasia", "cliente__razao_social")
    readonly_fields = ("num_pedido", "usuario", "data_cadastro", "total")

    def get_fornecedores(self, obj):
        return ", ".join(set(item.fornecedor.nome_fantasia for item in obj.itens.all()))

    get_fornecedores.short_description = "Fornecedor"  # Título da coluna

    def get_prazo_entrega(self, obj):
        return ", ".join(
            set(item.prazo_entrega.strftime("%d/%m/%Y") for item in obj.itens.all())
        )

    get_prazo_entrega.short_description = "Prazo Entrega"  # Título da coluna


admin.site.register(PedidoVenda, PedidoVendaAdmin)
admin.site.register(ItemPedido)
