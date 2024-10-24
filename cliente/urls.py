from django.urls import path
from . import views

app_name = "cliente"

urlpatterns = [
    path("", views.get_lista, name="lista"),
    path("<int:pk>/", views.get_detalhe, name="detalhe"),
    path("criar/", views.post_criar, name="post_criar"),
    path("<int:pk>/", views.put_editar, name="put_editar"),
]
