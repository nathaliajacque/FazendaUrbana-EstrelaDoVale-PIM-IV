from django.contrib import admin
from .models import Cliente


class ClienteAdmin(admin.ModelAdmin):
    list_filter = (
        "id_cliente",
        "status",
        "nome_fantasia",
        "razao_social",
        "cnpj",
        "contato",
        "data_cadastro",
    )
    search_fields = (
        "id_cliente",
        "status",
        "nome_fantasia",
        "razao_social",
        "cnpj",
        "email_1",
        "contato",
    )
    readonly_fields = ("id_cliente", "data_cadastro", "usuario")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)

    class Meta:
        verbose_name = "Cliente"
        verbose_name_plural = "Clientes"


admin.site.register(Cliente, ClienteAdmin)
