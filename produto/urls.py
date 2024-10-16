from django.urls import path
from . import views

app_name = "produto"

urlpatterns = [
    path("", views.ListaProdutos.as_view(), name="lista"),
]
