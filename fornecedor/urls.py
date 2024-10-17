from django.urls import path
from . import views

app_name = "fornecedor"

urlpatterns = [
    path("", views.ListaFornecedor.as_view(), name="lista"),
    path("<int:pk>/", views.DetalheFornecedor.as_view(), name="detalhe"),
    path("cria/", views.CriaFornecedor.as_view(), name="criar"),
    path("<int:pk>/", views.EditaFornecedor.as_view(), name="editar"),
]
