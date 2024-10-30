from django.http import JsonResponse, HttpResponseNotAllowed
import json
from .models import Pedido, Cliente
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from utils.decorators import (
    gerente_required,
    funcionario_required,
)
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
        filters = build_filters(Pedido, request.GET)
        querySet = Pedido.objects.filter(filters)
        serialized_data = serialize_queryset(Pedido, querySet)
        return JsonResponse(serialized_data, safe=False)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)


@funcionario_required
@login_required_middleware
def get_detalhe(request, pk):
    try:
        pedido = Pedido.objects.get(pk=pk)
    except Pedido.DoesNotExist:
        return JsonResponse({"erro": "Pedido não encontrado"}, status=404)

    data = pedido.__dict__
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
        cliente_id = data.pop("cliente", None)

        if not usuario_id or not cliente_id:
            return JsonResponse(
                {"erro": "Usuário e cliente são obrigatórios"}, status=400
            )

        usuario = Usuario.objects.get(id=usuario_id)
        cliente = Cliente.objects.get(id=cliente_id)

        # Forçar o valor do campo `status` como "EM_ANDAMENTO"
        data["status"] = "EM_ANDAMENTO"

        pedido = Pedido.objects.create(usuario=usuario, cliente=cliente, **data)
        return JsonResponse({"id": pedido.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"erro": "Corpo da requisição inválido"}, status=400)
    except Usuario.DoesNotExist:
        return JsonResponse({"erro": "Usuário não encontrado"}, status=404)
    except Cliente.DoesNotExist:
        return JsonResponse({"erro": "Cliente não encontrado"}, status=404)
    except ValidationError as e:
        return JsonResponse({"erro": e.message_dict}, status=400)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)


@csrf_exempt
@funcionario_required
@login_required_middleware
def put_editar(request, pk):
    if request.method != "PUT":
        return HttpResponseNotAllowed(["PUT"], "Método não permitido")

    try:
        data = json.loads(request.body)
        pedido = Pedido.objects.get(pk=pk)

        # Verificar se o campo `status` está presente e validar o valor
        if "status" in data and data["status"] not in [
            "EM_ANDAMENTO",
            "CONCLUIDO",
            "CANCELADO",
        ]:
            return JsonResponse(
                {
                    "erro": "Status inválido. Permitidos apenas 'EM_ANDAMENTO', 'CONCLUIDO' e 'CANCELADO'."
                },
                status=400,
            )

        for key, value in data.items():
            if hasattr(pedido, key):
                setattr(pedido, key, value)
            else:
                return JsonResponse(
                    {"erro": f"Atributo '{key}' não é válido"}, status=400
                )

        pedido.full_clean()
        pedido.save()
        return JsonResponse({"id": pedido.id}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"erro": "Corpo da requisição inválido"}, status=400)
    except Pedido.DoesNotExist:
        return JsonResponse({"erro": "Pedido não encontrado"}, status=404)
    except ValidationError as e:
        return JsonResponse({"erro": e.message_dict}, status=400)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)
