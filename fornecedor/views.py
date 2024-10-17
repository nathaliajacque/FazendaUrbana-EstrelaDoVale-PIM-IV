from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views import View
from . import models


class ListaFornecedor(ListView):
    model = models.Fornecedor


class DetalheFornecedor(DetailView):
    pass


class CriaFornecedor(View):
    pass


class EditaFornecedor(View):
    pass
