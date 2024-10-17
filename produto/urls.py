from django.urls import path
from . import views

app_name = "produto"

urlpatterns = [
    path("", views.get_lista),
    path("<int:pk>/", views.get_detalhe),
    path("criar/", views.post_criar),
    path("editar/<int:pk>/", views.put_editar)
]
