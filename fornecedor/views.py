from django.http import JsonResponse, HttpResponseNotAllowed
import json
from .models import Fornecedor
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
        filters = build_filters(Fornecedor, request.GET)
        querySet = Fornecedor.objects.filter(filters)
        serialized_data = serialize_queryset(Fornecedor, querySet)
        return JsonResponse(serialized_data, safe=False)
    except Exception as e:
        return JsonResponse({"erro": f"Erro inesperado {str(e)}"}, status=500)


@funcionario_required
@login_required_middleware
def get_detalhe(request, pk):
    try:
        fornecedor = Fornecedor.objects.get(pk=pk)  # Tenta obter o fornecedor
    except Fornecedor.DoesNotExist:
        return JsonResponse({"erro": "Fornecedor não encontrado"}, status=404)

    data = fornecedor.__dict__
    data.pop("_state")  # Remove o campo _state que não é necessário
    return JsonResponse(data, safe=False)


@csrf_exempt
@gerente_required
@login_required_middleware
def post_criar(request):
    """
    Cria um novo fornecedor.

    Este método cria um novo fornecedor com base nos dados fornecidos na requisição.
    O ID do usuário deve ser fornecido nos dados da requisição.

    Args:
        request (HttpRequest): A requisição HTTP.

    Returns:
        JsonResponse: Uma resposta JSON com o ID do fornecedor criado ou uma mensagem de erro.
    """
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

        # Instancia um objeto do tipo Fornecedor, agora com a instância de usuario
        fornecedor = Fornecedor(usuario=usuario, **data)

        fornecedor.full_clean()  # Valida os dados do objeto
        fornecedor.save()  # Salva o objeto no banco de dados
        return JsonResponse({"id": fornecedor.id}, status=201)

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
    """
    Edita um fornecedor existente.

    Este método edita um fornecedor existente com base nos dados fornecidos na requisição.
    O ID do fornecedor deve ser fornecido na URL.

    Args:
        request (HttpRequest): A requisição HTTP.
        pk (int): O ID do fornecedor a ser editado.

    Returns:
        JsonResponse: Uma resposta JSON com o ID do fornecedor editado ou uma mensagem de erro.
    """
    if request.method != "PUT":
        return HttpResponseNotAllowed(["PUT"], "Método não permitido")

    try:
        data = json.loads(request.body)
        fornecedor = Fornecedor.objects.get(pk=pk)

        for key, value in data.items():
            if hasattr(fornecedor, key):
                setattr(fornecedor, key, value)
            else:
                return JsonResponse(
                    {"erro": f"Atributo '{key}' não é válido"}, status=400
                )

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
