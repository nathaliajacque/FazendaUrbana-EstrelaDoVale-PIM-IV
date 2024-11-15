from django.http import JsonResponse, HttpResponseNotAllowed
import json
from .models import Cliente
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from utils.decorators import (
    gerente_required,
    funcionario_required,
)
from django.core.exceptions import ValidationError
from utils.middlewares import (
    build_filters,
    serialize_queryset,
    login_required_middleware,
)

Usuario = get_user_model()


@funcionario_required
@login_required_middleware
def get_lista(request):
    try:
        filters = build_filters(Cliente, request.GET)
        querySet = Cliente.objects.filter(filters)
        serialized_data = serialize_queryset(Cliente, querySet)
        return JsonResponse(serialized_data, safe=False)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)


@funcionario_required
@login_required_middleware
def get_detalhe(request, pk):
    try:
        cliente = Cliente.objects.get(pk=pk)
    except Cliente.DoesNotExist:
        return JsonResponse({"erro": "Cliente não encontrado"}, status=404)

    data = cliente.__dict__
    data.pop("_state")
    return JsonResponse(data, safe=False)


@csrf_exempt
@gerente_required
@login_required_middleware
def post_criar(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Método não permitido")

    try:
        data = json.loads(request.body)
        usuario_id = data.pop("usuario", None)

        if not usuario_id:
            return JsonResponse({"erro": "Usuário não informado"}, status=400)

        try:
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return JsonResponse({"erro": "Usuário não encontrado"}, status=400)

        cliente = Cliente(usuario=usuario, **data)
        cliente.full_clean()
        cliente.save()
        return JsonResponse({"id": cliente.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"erro": "Corpo da requisição inválido"}, status=400)
    except ValidationError as e:
        return JsonResponse({"erro": e.message_dict}, status=400)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)


@csrf_exempt
@gerente_required
@login_required_middleware
def put_editar(request, pk):
    if request.method != "PUT":
        return HttpResponseNotAllowed(["PUT"], "Método não permitido")

    try:
        data = json.loads(request.body)
        cliente = Cliente.objects.get(pk=pk)

        for key, value in data.items():
            if hasattr(cliente, key):
                setattr(cliente, key, value)
            else:
                return JsonResponse(
                    {"erro": f"Atributo '{key}' não é válido"}, status=400
                )

        cliente.full_clean()
        cliente.save()
        return JsonResponse({"id": cliente.id}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"erro": "Corpo da requisição inválido"}, status=400)
    except Cliente.DoesNotExist:
        return JsonResponse({"erro": "Cliente não encontrado"}, status=404)
    except ValidationError as e:
        return JsonResponse({"erro": e.message_dict}, status=400)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)
