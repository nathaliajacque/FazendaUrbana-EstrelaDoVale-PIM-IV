from django.http import JsonResponse
from django.contrib.auth.decorators import user_passes_test


def administrador_required(view_func):
    decorated_view_func = user_passes_test(
        lambda user: user.is_authenticated and user.is_administrador(),
        login_url="/login/",
        redirect_field_name=None,
    )(view_func)
    return decorated_view_func


def gerente_required(view_func):
    decorated_view_func = user_passes_test(
        lambda user: user.is_authenticated
        and (user.is_administrador() or user.is_gerente()),
        login_url="/login/",
        redirect_field_name=None,
    )(view_func)
    return decorated_view_func


def funcionario_required(view_func):
    decorated_view_func = user_passes_test(
        lambda user: user.is_authenticated
        and (user.is_administrador() or user.is_gerente() or user.is_funcionario()),
        login_url="/login/",
        redirect_field_name=None,
    )(view_func)
    return decorated_view_func
