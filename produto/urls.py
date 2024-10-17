from django.urls import path
from . import views

app_name = "produto"

urlpatterns = [
    path("", views.get_list),
    path("<int:pk>/", views.get_detail),
    path("criar/", views.criar_produto),
    path("editar/<int:pk>/", views.editar_produto),
]
