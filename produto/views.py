from django.http import JsonResponse, HttpResponseBadRequest, HttpResponseNotAllowed
import json
from .models import Produto, Fornecedor, User
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from utils.middlewares import Middlewares


def get_list(request):
    try:
        filters = Middlewares.build_filters(Produto, request.GET)
        querySet = Produto.objects.filter(filters)
        serialized_data = Middlewares.serialize_queryset(Produto, querySet)
        return JsonResponse(serialized_data, safe=False)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)


def get_detail(request, pk):
    data = Produto.objects.get(pk=pk)
    data = data.__dict__
    data.pop("_state")
    return JsonResponse(data, safe=False)


@csrf_exempt
def criar_produto(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Método não permitido")

    try:
        data = json.loads(request.body)
        fornecedor = Fornecedor.objects.get(id=data["fornecedor"])
        data["fornecedor"] = fornecedor
        produto = Produto(**data)  # instancia um objeto do tipo Produto
        produto.full_clean()  # valida os dados do objeto
        produto.save()  # salva o objeto no banco de dados
        return JsonResponse({"id": produto.id}, status=201)

    except json.JSONDecodeError:
        return JsonResponse({"erro": "Corpo da requisição inválido"}, status=400)
    except ObjectDoesNotExist:
        return JsonResponse({"erro": "Fornecedor não encontrado"}, status=404)
    except ValidationError as e:
        return JsonResponse({"erro": e.message_dict}, status=400)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)


@csrf_exempt
def editar_produto(request, pk):
    if request.method != "PUT":
        return HttpResponseNotAllowed(["PUT"], "Método não permitido")

    try:
        data = json.loads(request.body)
        produto = Produto.objects.get(pk=pk)
        if "fornecedor" in data:
            fornecedor = Fornecedor.objects.get(id=data["fornecedor"])
            data["fornecedor"] = fornecedor

        for key, value in data.items():
            setattr(produto, key, value)
        produto.full_clean()
        produto.save()
        return JsonResponse({"id": produto.id}, status=200)

    except json.JSONDecodeError:
        return JsonResponse({"erro": "Corpo da requisição inválido"}, status=400)
    except ObjectDoesNotExist:
        return JsonResponse({"erro": "Produto não encontrado"}, status=404)
    except ValidationError as e:
        return JsonResponse({"erro": e.message_dict}, status=400)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)
