from django.urls import path
from . import views


app_name = "pedido"


urlpatterns = [
    path("", views.ListaPedido.as_view(), name="lista"),
    path("<int:pk>/", views.DetalhePedido.as_view(), name="detalhe"),
    path("cria/", views.CriaPedido.as_view(), name="criar"),
    path("<int:pk>/", views.EditaPedido.as_view(), name="editar"),
]
