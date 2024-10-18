from django.contrib import admin
from .models import Usuario
from utils.forms import UsuarioAdminForm


class UsuarioAdmin(admin.ModelAdmin):
    form = UsuarioAdminForm
    list_display = (
        "id",
        "nivel_acesso"
    )
    list_filter = ("id", "deve_redefinir_senha")
    search_fields = ("full_name", "email")
    readonly_fields = ("id", "date_joined", "username")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Usuario, UsuarioAdmin)
