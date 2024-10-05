from django.contrib import admin
from .models import Funcionario


class FuncionarioAdmin(admin.ModelAdmin):
    list_display = ("nome", "cargo", "cpf", "email", "data_cadastro")
    search_fields = ("nome", "cargo", "cpf", "email")
    list_filter = ("cargo", "cidade", "uf")
    readonly_fields = ("usuario", "data_cadastro", "id_funcionario")

    def save_model(self, request, obj, form, change):
        if not obj.pk:
            obj.usuario = request.user
        super().save_model(request, obj, form, change)


admin.site.register(Funcionario, FuncionarioAdmin)
