from django.contrib import admin
from .models import Usuario


# class UsuarioAdmin(admin.ModelAdmin):
#     list_display = ("id",)
#     list_filter = "id"
#     search_fields = ""
#     readonly_fields = "id"

#     def save_model(self, request, obj, form, change):
#         if not obj.pk:
#             obj.usuario = request.usuario
#         super().save_model(request, obj, form, change)


# admin.site.register(Usuario, UsuarioAdmin)
