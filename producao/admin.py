from django.contrib import admin
from .models import Producao
from pedido.models import ItemPedido
from .models import Pedido


class ItemPedidoInline(admin.TabularInline):
    model = ItemPedido
    extra = 0
    fields = ("produto", "quantidade", "fornecedor", "prazo_entrega")
    readonly_fields = ("produto", "quantidade", "fornecedor", "prazo_entrega")

    def get_queryset(self, request):
        qs = super().get_queryset(request)
        # Certifique-se de que o filtro usa a instância de Pedido e não de Produção
        if hasattr(self, "parent_model") and isinstance(self.parent_model, Pedido):
            return qs.filter(pedido=self.parent_model)
        return qs


class ProducaoAdmin(admin.ModelAdmin):
    list_display = (
        "id",
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
    search_fields = ("id", "cliente", "fornecedor")
    readonly_fields = (
        "data_cadastro",
        "usuario",
        "prazo_entrega",
    )  # Definir como readonly o campo usuário também

    inlines = [ItemPedidoInline]

    # Sobrescreve o método get_form para inicializar o prazo de entrega baseado no ItemPedido
    def get_form(self, request, obj=None, **kwargs):
        form = super().get_form(request, obj, **kwargs)
        if obj and obj.pedido:
            # Verifique se o campo 'prazo_entrega' está presente no formulário
            if "prazo_entrega" in form.base_fields:
                # Obtém o prazo de entrega do primeiro item do pedido
                item_pedido = obj.pedido.itens.first()
                if item_pedido:
                    form.base_fields["prazo_entrega"].initial = (
                        item_pedido.prazo_entrega
                    )
        return form

    def save_model(self, request, obj, form, change):
        if not change:  # Se for uma nova instância
            if obj.pedido:  # Verifique se o pedido está associado
                item_pedido = (
                    obj.pedido.itens.first()
                )  # Obtém o primeiro item do pedido
                if item_pedido:
                    obj.prazo_entrega = (
                        item_pedido.prazo_entrega
                    )  # Usa o prazo do primeiro item
                obj.usuario = request.user  # Atribui o objeto do usuário
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

    # produtos_list.short_description = "Produtos do Pedido"


admin.site.register(Producao, ProducaoAdmin)
