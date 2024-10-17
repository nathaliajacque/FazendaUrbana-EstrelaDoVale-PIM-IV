from django.urls import path
from . import views

app_name = "producao"

urlpatterns = [
    path("", views.ListaProducao.as_view(), name="lista"),
    path("<int:pk>/", views.DetalheProducao.as_view(), name="detalhe"),
    path("cria/", views.CriaProducao.as_view(), name="criar"),
    path("<int:pk>/", views.EditaProducao.as_view(), name="editar"),
]
