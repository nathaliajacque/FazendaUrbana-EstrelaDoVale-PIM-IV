from django.contrib import admin
from .models import Pedido
from .models import ItemPedido


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
        "cliente",
        "data_venda",
        "total",
        "status",
        "usuario",
        "data_cadastro",
    )
    list_filter = ("status", "data_venda", "data_cadastro")
    search_fields = ("id", "cliente", "prazo_entrega")
    readonly_fields = ("id", "usuario", "data_cadastro", "total")

    def save_model(self, request, obj, form, change):
        if not change:  # Se for uma nova instância
            obj.status = "EM_ANDAMENTO"  # Define o status como "EM_ANDAMENTO"
        super().save_model(request, obj, form, change)

    def get_fornecedores(self, obj):
        return ", ".join(set(item.fornecedor.nome_fantasia for item in obj.itens.all()))

    def get_prazo_entrega(self, obj):
        return ", ".join(
            set(item.prazo_entrega.strftime("%d/%m/%Y") for item in obj.itens.all())
        )

    get_fornecedores.short_description = "Fornecedor"  # Título da coluna

    get_prazo_entrega.short_description = "Prazo Entrega"  # Título da coluna


admin.site.register(Pedido, PedidoAdmin)
admin.site.register(ItemPedido)
