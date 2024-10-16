from django.contrib import admin
from .models import Usuario
from utils.forms import UsuarioAdminForm


class UsuarioAdmin(admin.ModelAdmin):
    form = UsuarioAdminForm
    list_display = (
        "id",
        "status",
        "nome",
        "login",
        "nivel_acesso",
        "data_cadastro",
    )
    list_filter = ("id", "data_cadastro", "deve_redefinir_senha")
    search_fields = ("nome", "login")
    readonly_fields = ("id", "data_cadastro", "usuario")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Usuario, UsuarioAdmin)
