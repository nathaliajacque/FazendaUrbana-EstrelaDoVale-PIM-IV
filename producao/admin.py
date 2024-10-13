from django.contrib import admin
from .models import Producao
from pedido.models import ItemPedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    fields = ("produto", "quantidade", "fornecedor", "prazo_entrega")
    readonly_fields = ("produto", "quantidade", "fornecedor", "prazo_entrega")
    can_delete = False
    show_change_link = False


class ProducaoAdmin(admin.ModelAdmin):
    list_display = (
        "id_producao",
        "pedido",
        "cliente",
        "status",
        "data_inicio",
        "prazo_entrega",
        "controle_ambiente",
        "usuario",
        "data_cadastro",
    )
    list_filter = ("status", "data_inicio", "data_cadastro")
    search_fields = ("id_producao", "pedido__id_pedido", "cliente__nome_fantasia")
    readonly_fields = (
        "data_cadastro",
        "usuario",
        "prazo_entrega",
    )  # Definir como readonly o campo usuário também

    inlines = [ItemPedidoInline]

    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.pedido:
            form.base_fields["prazo_entrega"].initial = (
                obj.pedido.calcular_prazo_entrega()
            )
        return form

    def save_model(self, request, obj, form, change):
        if not change:  # Se for uma nova instância
            obj.prazo_entrega = obj.pedido.calcular_prazo_entrega()
        obj.usuario = (
            request.user
        )  # Atribui o objeto do usuário ao invés de username como string
        super().save_model(request, obj, form, change)

    def produtos_list(self, obj):
        if obj.pedido:
            return ", ".join(
                [
                    f"{item.produto.descricao} - {item.quantidade} unidade(s)"
                    for item in obj.pedido.itens.all()
                ]
            )
        return "Sem produtos"

    produtos_list.short_description = "Produtos do Pedido"


admin.site.register(Producao, ProducaoAdmin)
