from django.db.models import Q
from rest_framework import serializers
from django.http import JsonResponse
from functools import wraps
from rest_framework_simplejwt.authentication import JWTAuthentication
from rest_framework_simplejwt.exceptions import InvalidToken, TokenError


def build_filters(model, query_params):
    filters = Q()

    for key, value in query_params.items():
        if hasattr(model, key):
            filters &= Q(**{f"{key}__icontains": value})

    return filters


def serialize_queryset(model, queryset):
    GenericSerializer = type(
        "GenericSerializer",
        (serializers.ModelSerializer,),
        {"Meta": type("Meta", (object,), {"model": model, "fields": "__all__"})},
    )

    serializer = GenericSerializer(queryset, many=True)
    return serializer.data


def login_required_middleware(view_func):
    @wraps(view_func)
    def middleware(request, *args, **kwargs):
        auth = JWTAuthentication()
        try:
            user, token = auth.authenticate(request)
            if user is None:
                raise InvalidToken("Token inválido ou expirado")
            request.user = user
        except (InvalidToken, TokenError) as e:
            return JsonResponse({"erro": str(e)}, status=401)
        return view_func(request, *args, **kwargs)

    return middleware
