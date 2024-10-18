from django.db.models import Q
from rest_framework import serializers
from django.http import JsonResponse


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

def login_required_middleware(get_response):
    def middleware(request):
        if request.path in ["/login/", "/logout/"]:
            return get_response(request)
        if not request.user.is_authenticated:
            return JsonResponse({"erro": "Usuário não autenticado"}, status=401)
        return get_response(request)
    return middleware