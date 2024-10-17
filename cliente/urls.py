from django.urls import path
from . import views

app_name = "cliente"

urlpatterns = [
    path("", views.ListaCliente.as_view(), name="lista"),
    path("<int:pk>/", views.DetalheCliente.as_view(), name="detalhe"),
    path("cria/", views.CriaCliente.as_view(), name="criar"),
    path("<int:pk>/", views.EditaCliente.as_view(), name="editar"),
]
