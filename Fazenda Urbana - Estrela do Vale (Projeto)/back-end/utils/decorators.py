from django.http import JsonResponse


def administrador_required(view_func):
    def check_user(user):
        if user.is_superuser:
            return True
        return user.is_authenticated and (user.is_administrador())

    def wrapped_view(request, *args, **kwargs):
        if not check_user(request.user):
            return JsonResponse(
                {"error": "Usuário não tem permissão para acessar esta rota."},
                status=403,
            )
        return view_func(request, *args, **kwargs)

    return wrapped_view


def gerente_required(view_func):
    def check_user(user):
        if user.is_superuser:
            return True
        return user.is_authenticated and (user.is_administrador() or user.is_gerente())

    def wrapped_view(request, *args, **kwargs):
        if not check_user(request.user):
            return JsonResponse(
                {"error": "Usuário não tem permissão para acessar esta rota."},
                status=403,
            )
        return view_func(request, *args, **kwargs)

    return wrapped_view


def funcionario_required(view_func):
    def check_user(user):
        if user.is_superuser:
            return True
        return user.is_authenticated and (
            user.is_administrador() or user.is_gerente() or user.is_funcionario()
        )

    def wrapped_view(request, *args, **kwargs):
        if not check_user(request.user):
            return JsonResponse(
                {"error": "Usuário não tem permissão para acessar esta rota."},
                status=403,
            )
        return view_func(request, *args, **kwargs)

    return wrapped_view
