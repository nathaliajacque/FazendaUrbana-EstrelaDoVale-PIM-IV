from django.urls import path
from . import views

app_name = "funcionario"

urlpatterns = [
    path("", views.ListaFuncionario.as_view(), name="lista"),
    path("<int:pk>/", views.DetalheFuncionario.as_view(), name="detalhe"),
    path("cria/", views.CriaFuncionario.as_view(), name="criar"),
    path("<int:pk>/", views.EditaFuncionario.as_view(), name="editar"),
]
