from django.contrib import admin
from .models import Usuario
from utils.forms import UsuarioAdminForm


class UsuarioAdmin(admin.ModelAdmin):
    form = UsuarioAdminForm
    list_display = (
        "id_usuario",
        "nome",
        "login",
        "data_cadastro",
        "deve_redefinir_senha",
    )
    list_filter = ("data_cadastro", "deve_redefinir_senha")
    search_fields = ("nome", "login")
    readonly_fields = ("id_usuario", "data_cadastro", "usuario")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Usuario, UsuarioAdmin)
