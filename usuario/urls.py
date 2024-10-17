from django.urls import path
from . import views


app_name = "usuario"


urlpatterns = [
    path("", views.ListaUsuario.as_view(), name="lista"),
    path("<int:pk>/", views.DetalheUsuario.as_view(), name="detalhe"),
    path("cria/", views.CriaUsuario.as_view(), name="criar"),
    path("<int:pk>/", views.EditaUsuario.as_view(), name="editar"),
    path("login/", views.Login.as_view, name="login"),
    path("logout/", views.Logout.as_view, name="logout"),
]
