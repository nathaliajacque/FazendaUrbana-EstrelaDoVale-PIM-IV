from django.contrib.auth.decorators import user_passes_test
from django.contrib.auth import authenticate, login, logout
from django.http import JsonResponse, HttpResponseNotAllowed
import json
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from utils.middlewares import (
    build_filters,
    serialize_queryset,
    login_required_middleware,
)

Usuario = get_user_model()


@login_required_middleware
def get_lista(request):
    try:
        filters = build_filters(Usuario, request.GET)
        querySet = Usuario.objects.filter(filters)
        serialized_data = serialize_queryset(Usuario, querySet)
        return JsonResponse(serialized_data, safe=False)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)


@login_required_middleware
def get_detalhe(request, pk):
    try:
        usuario = Usuario.objects.get(pk=pk)  # Tenta obter o fornecedor
    except Usuario.DoesNotExist:
        return JsonResponse({"erro": "Usuário não encontrado"}, status=404)

    data = usuario.__dict__
    data.pop("_state")  # Remove o campo _state que não é necessário
    return JsonResponse(data, safe=False)


@csrf_exempt
@login_required_middleware
def post_criar(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Método não permitido")

    try:
        data = json.loads(request.body)
        email = data.pop("email", None)
        password = data.pop("password", None)

        if not email or not password:
            return JsonResponse({"erro": "Email e senha são obrigatórios"}, status=400)

        # Cria o usuário usando o método create_user
        usuario = Usuario.objects.create_user(email=email, password=password, **data)
        return JsonResponse({"id": usuario.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"erro": "Corpo da requisição inválido"}, status=400)
    except ValidationError as e:
        return JsonResponse({"erro": e.message_dict}, status=400)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)


@csrf_exempt
@login_required_middleware
def put_editar(request, pk):
    if request.method != "PUT":
        return HttpResponseNotAllowed(["PUT"], "Método não permitido")

    try:
        data = json.loads(request.body)
        usuario = Usuario.objects.get(pk=pk)

        for key, value in data.items():
            setattr(usuario, key, value)
        usuario.full_clean()
        usuario.save()
        return JsonResponse({"id": usuario.id}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"erro": "Corpo da requisição inválido"}, status=400)
    except Usuario.DoesNotExist:
        return JsonResponse({"erro": "Usuário não encontrado"}, status=404)
    except ValidationError as e:
        return JsonResponse({"erro": e.message_dict}, status=400)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)


@csrf_exempt
def user_login(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Método não permitido")

    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JsonResponse({"erro": "Email e senha são obrigatórios"}, status=400)
        user = authenticate(request, email=email, password=password)

        if user is not None:
            login(request, user)
            return JsonResponse({"message": "Login realizado com sucesso"}, status=200)
        else:
            return JsonResponse({"erro": "Credenciais inválidas"}, status=400)

    except json.JSONDecodeError:
        return JsonResponse({"erro": "Corpo da requisição inválido"}, status=400)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)


@csrf_exempt
@login_required_middleware
def user_logout(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Método não permitido")

    try:
        data = json.loads(request.body)
        email = data.get("email")
        password = data.get("password")

        if not email or not password:
            return JsonResponse({"erro": "Email e senha são obrigatórios"}, status=400)

        logout(request)
        return JsonResponse({"message": "Logout realizado com sucesso"}, status=200)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)


def administrador_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and u.is_administrador(), login_url="/login/"
    )(view_func)
    return decorated_view_func


def gerente_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and (u.is_administrador() or u.is_gerente()),
        login_url="/login/",
    )(view_func)
    return decorated_view_func


def funcionario_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated
        and (u.is_administrador() or u.is_gerente() or u.is_funcionario()),
        login_url="/login/",
    )(view_func)
    return decorated_view_func
