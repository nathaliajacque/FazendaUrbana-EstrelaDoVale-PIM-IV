from django.http import JsonResponse, HttpResponseNotAllowed
import json
from .models import Producao, Pedido, Cliente
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
        filters = build_filters(Producao, request.GET)
        querySet = Producao.objects.filter(filters)
        serialized_data = serialize_queryset(Producao, querySet)
        return JsonResponse(serialized_data, safe=False)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)


@login_required_middleware
def get_detalhe(request, pk):
    try:
        producao = Producao.objects.get(pk=pk)
    except Producao.DoesNotExist:
        return JsonResponse({"erro": "Produção não encontrada"}, status=404)

    data = producao.__dict__
    data.pop("_state")
    return JsonResponse(data, safe=False)


@csrf_exempt
@login_required_middleware
def post_criar(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Método não permitido")

    try:
        data = json.loads(request.body)
        usuario_id = data.pop("usuario", None)
        pedido_id = data.pop("pedido", None)
        cliente_id = data.pop("cliente", None)

        if not usuario_id or not pedido_id or not cliente_id:
            return JsonResponse(
                {"erro": "Usuário, pedido e cliente são obrigatórios"}, status=400
            )

        usuario = Usuario.objects.get(id=usuario_id)
        pedido = Pedido.objects.get(id=pedido_id)
        cliente = Cliente.objects.get(id=cliente_id)

        producao = Producao.objects.create(
            usuario=usuario, pedido=pedido, cliente=cliente, **data
        )
        return JsonResponse({"id": producao.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"erro": "Corpo da requisição inválido"}, status=400)
    except Usuario.DoesNotExist:
        return JsonResponse({"erro": "Usuário não encontrado"}, status=404)
    except Pedido.DoesNotExist:
        return JsonResponse({"erro": "Pedido não encontrado"}, status=404)
    except Cliente.DoesNotExist:
        return JsonResponse({"erro": "Cliente não encontrado"}, status=404)
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
        producao = Producao.objects.get(pk=pk)

        for key, value in data.items():
            if hasattr(producao, key):
                setattr(producao, key, value)
            else:
                return JsonResponse(
                    {"erro": f"Atributo '{key}' não é válido"}, status=400
                )

        producao.full_clean()
        producao.save()
        return JsonResponse({"id": producao.id}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"erro": "Corpo da requisição inválido"}, status=400)
    except Producao.DoesNotExist:
        return JsonResponse({"erro": "Produção não encontrada"}, status=404)
    except ValidationError as e:
        return JsonResponse({"erro": e.message_dict}, status=400)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)
