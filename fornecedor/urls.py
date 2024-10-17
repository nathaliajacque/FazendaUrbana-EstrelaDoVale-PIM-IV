from django.urls import path
from . import views

app_name = "fornecedor"

urlpatterns = [
    path("", views.get_lista, name='get_lista'),
    path("<int:pk>/", views.get_detalhe, name='get_detalhe'),
    path("criar/", views.post_criar, name='post_criar'),
    path("editar/<int:pk>/", views.put_editar, name='put_editar')
]
