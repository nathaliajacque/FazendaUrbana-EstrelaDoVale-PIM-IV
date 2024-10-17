from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
import json
from .models import  Fornecedor, User
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from utils.middlewares import Middlewares


def get_lista(request):
    try:
        filters = Middlewares.build_filters(Fornecedor, request.GET)
        querySet = Fornecedor.objects.filter(filters)
        serialized_data = Middlewares.serialize_queryset(Fornecedor, querySet)
        return JsonResponse(serialized_data, safe=False)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)

def get_detalhe(request, pk):
    try:
        fornecedor = Fornecedor.objects.get(pk=pk)  # Tenta obter o fornecedor
    except Fornecedor.DoesNotExist:
        return JsonResponse({"erro": "Fornecedor não encontrado"}, status=404)

    data = fornecedor.__dict__
    data.pop("_state")  # Remove o campo _state que não é necessário
    return JsonResponse(data, safe=False)


@csrf_exempt
def post_criar(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Método não permitido")

    try:
        data = json.loads(request.body)
        fornecedor = Fornecedor(**data)  # instancia um objeto do tipo Produto
        fornecedor.full_clean()  # valida os dados do objeto
        fornecedor.save()  # salva o objeto no banco de dados
        return JsonResponse({"id": fornecedor.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"erro": "Corpo da requisição inválido"}, status=400)
    except ValidationError as e:
        return JsonResponse({"erro": e.message_dict}, status=400)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)


@csrf_exempt
def put_editar(request, pk):
    if request.method != "PUT":
        return HttpResponseNotAllowed(["PUT"], "Método não permitido")

    try:
        data = json.loads(request.body)
        fornecedor = Fornecedor.objects.get(pk=pk)

        for key, value in data.items():
            setattr(fornecedor, key, value)
        fornecedor.full_clean()
        fornecedor.save()
        return JsonResponse({"id": fornecedor.id}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"erro": "Corpo da requisição inválido"}, status=400)
    except Fornecedor.DoesNotExist:
        return JsonResponse({"erro": "Fornecedor não encontrado"}, status=404)
    except ValidationError as e:
        return JsonResponse({"erro": e.message_dict}, status=400)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)
