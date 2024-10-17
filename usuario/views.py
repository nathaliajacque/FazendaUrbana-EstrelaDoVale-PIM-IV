from django.shortcuts import render
from django.contrib.auth.decorators import user_passes_test
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views import View
from . import models


class ListaUsuario(ListView):
    model = models.Usuario


class DetalheUsuario(DetailView):
    pass


class CriaUsuario(View):
    pass


class EditaUsuario(View):
    pass


class Login(View):
    pass


class Logout(View):
    pass


def administrador_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and u.is_administrador(), login_url="/login/"
    )(view_func)
    return decorated_view_func


def gerente_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated and (u.is_administrador() or u.is_gerente()),
        login_url="/login/",
    )(view_func)
    return decorated_view_func


def funcionario_required(view_func):
    decorated_view_func = user_passes_test(
        lambda u: u.is_authenticated
        and (u.is_administrador() or u.is_gerente() or u.is_funcionario()),
        login_url="/login/",
    )(view_func)
    return decorated_view_func
