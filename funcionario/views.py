from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views import View
from . import models


class ListaFuncionario(ListView):
    model = models.Funcionario


class DetalheFuncionario(DetailView):
    pass


class CriaFuncionario(View):
    pass


class EditaFuncionario(View):
    pass
