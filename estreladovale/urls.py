"""
URL configuration for estreladovale project.

The `urlpatterns` list routes URLs to views. For more information please see:
    https://docs.djangoproject.com/en/5.1/topics/http/urls/
Examples:
Function views
    1. Add an import:  from my_app import views
    2. Add a URL to urlpatterns:  path('', views.home, name='home')
Class-based views
    1. Add an import:  from other_app.views import Home
    2. Add a URL to urlpatterns:  path('', Home.as_view(), name='home')
Including another URLconf
    1. Import the include() function: from django.urls import include, path
    2. Add a URL to urlpatterns:  path('blog/', include('blog.urls'))
"""

from django.contrib import admin
from django.urls import path, include
from django.conf import settings
from django.conf.urls.static import static
from usuario.views import user_login, user_logout
from django.http import JsonResponse


def health_check(request):
    return JsonResponse({"status": "ok"}, status=200)
urlpatterns = [
    # O caracter "" indica que a URL raiz será a URL do app produto
    path("produtos/", include("produto.urls")),
    path("usuarios/", include("usuario.urls")),
    path("login/", user_login, name="login"),
    path("logout/", user_logout, name="logout"),
    path("pedidos/", include("pedido.urls")),
    path("producoes/", include("producao.urls")),
    path("fornecedores/", include("fornecedor.urls")),
    path("clientes/", include("cliente.urls")),
    path("funcionarios/", include("funcionario.urls")),
    path("admin/", admin.site.urls),
    path("healthcheck/", health_check, name="health_check"),
] + static(settings.MEDIA_URL, document_root=settings.MEDIA_ROOT)
