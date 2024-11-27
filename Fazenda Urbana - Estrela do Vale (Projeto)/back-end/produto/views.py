from django.http import JsonResponse, HttpResponseNotAllowed
import json
from .models import Produto, Fornecedor
from django.contrib.auth import get_user_model
from django.views.decorators.csrf import csrf_exempt
from django.core.exceptions import ValidationError, ObjectDoesNotExist
from utils.decorators import gerente_required, funcionario_required
from utils.middlewares import (
    build_filters,
    serialize_queryset,
    login_required_middleware,
)

Usuario = get_user_model()

@login_required_middleware
@funcionario_required
def get_lista(request):
    try:
        filters = build_filters(Produto, request.GET)
        querySet = Produto.objects.filter(filters)
        serialized_data = serialize_queryset(Produto, querySet)
        return JsonResponse(serialized_data, safe=False)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)


@login_required_middleware
@funcionario_required
def get_detalhe(request, pk):
    try:
        produto = Produto.objects.get(pk=pk)  # Tenta obter o produto
    except Produto.DoesNotExist:
        return JsonResponse({"erro": "Produto não encontrado"}, status=404)
    data = produto.__dict__
    data.pop("_state")
    return JsonResponse(data, safe=False)


@csrf_exempt
@login_required_middleware
@gerente_required
def post_criar(request):
    if request.method != "POST":
        return HttpResponseNotAllowed(["POST"], "Método não permitido")

    try:
        data = json.loads(request.body)

        # Pega o ID do usuário
        usuario_id = data.pop("usuario", None)

        if not usuario_id:
            return JsonResponse({"erro": "Usuário não informado"}, status=400)
        
        try:
            # Busca a instância do usuário pelo ID
            usuario = Usuario.objects.get(id=usuario_id)
        except Usuario.DoesNotExist:
            return JsonResponse({"erro": "Usuário não encontrado"}, status=400)
        

         # Pega o ID do fornecedor
        fornecedor_id = data.pop("fornecedor", None)

        if not fornecedor_id:
            return JsonResponse({"erro": "Fornecedor não informado"}, status=400)

        try:
            # Busca a instância do fornecedor pelo ID
            fornecedor = Fornecedor.objects.get(id=fornecedor_id)
        except Fornecedor.DoesNotExist:
            return JsonResponse({"erro": "Fornecedor não encontrado"}, status=400)

        # Instancia um objeto do tipo Produto, agora com a instância de usuario e fornecedor
        produto = Produto(usuario=usuario, fornecedor=fornecedor, **data)
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
@login_required_middleware
@gerente_required
def put_editar(request, pk):
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
    except Produto.DoesNotExist:
        return JsonResponse({"erro": "Produto não encontrado"}, status=404)
    except ValidationError as e:
        return JsonResponse({"erro": e.message_dict}, status=400)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)
