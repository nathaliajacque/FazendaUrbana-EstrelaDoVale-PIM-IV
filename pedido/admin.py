from django.contrib import admin
from .models import PedidoVenda
from .models import ItemPedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 1


class PedidoVendaAdmin(admin.ModelAdmin):
    inlines = [ItemPedidoInline]
    list_display = (
        "num_pedido",
        "status",
        "data_venda",
        "data_cadastro",
        "usuario",
        "cliente",
        "prazo_entrega",
    )
    list_filter = ("status", "data_venda", "data_cadastro")
    search_fields = ("num_pedido", "cliente__nome_fantasia", "cliente__razao_social")
    readonly_fields = ("num_pedido", "usuario", "data_cadastro")


admin.site.register(PedidoVenda, PedidoVendaAdmin)
admin.site.register(ItemPedido)
