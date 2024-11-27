from django.http import JsonResponse, HttpResponseNotAllowed
import json
from .models import Funcionario
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError
from utils.decorators import gerente_required
from utils.middlewares import (
    build_filters,
    serialize_queryset,
    login_required_middleware,
)


Usuario = get_user_model()


@login_required_middleware
@gerente_required
def get_lista(request):
    try:
        filters = build_filters(Funcionario, request.GET)
        querySet = Funcionario.objects.filter(filters)
        serialized_data = serialize_queryset(Funcionario, querySet)
        return JsonResponse(serialized_data, safe=False)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)


@login_required_middleware
@gerente_required
def get_detalhe(request, pk):
    try:
        funcionario = Funcionario.objects.get(pk=pk)  # Tenta obter o funcionário
    except Funcionario.DoesNotExist:
        return JsonResponse({"erro": "Funcionário não encontrado"}, status=404)

    data = funcionario.__dict__
    data.pop("_state")  # Remove o campo _state que não é necessário
    return JsonResponse(data, safe=False)


@csrf_exempt
@login_required_middleware
@gerente_required
def post_criar(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Método não permitido")

    try:
        data = json.loads(request.body)
        funcionario = Funcionario(**data)  # instancia um objeto do tipo Funcionario
        funcionario.full_clean()  # valida os dados do objeto
        funcionario.save()  # salva o objeto no banco de dados
        return JsonResponse({"id": funcionario.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"erro": "Corpo da requisição inválido"}, status=400)
    except ValidationError as e:
        return JsonResponse({"erro": e.message_dict}, status=400)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)


@csrf_exempt
@login_required_middleware
@gerente_required
def put_editar(request, pk):
    if request.method != "PUT":
        return HttpResponseNotAllowed(["PUT"], "Método não permitido")

    try:
        data = json.loads(request.body)
        funcionario = Funcionario.objects.get(pk=pk)

        for key, value in data.items():
            setattr(funcionario, key, value)
        funcionario.full_clean()
        funcionario.save()
        return JsonResponse({"id": funcionario.id}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"erro": "Corpo da requisição inválido"}, status=400)
    except Funcionario.DoesNotExist:
        return JsonResponse({"erro": "Funcionário não encontrado"}, status=404)
    except ValidationError as e:
        return JsonResponse({"erro": e.message_dict}, status=400)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)
