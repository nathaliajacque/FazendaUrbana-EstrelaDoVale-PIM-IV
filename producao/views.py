from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views import View
from . import models


class ListaProducao(ListView):
    model = models.Producao


class DetalheProducao(DetailView):
    pass


class CriaProducao(View):
    pass


class EditaProducao(View):
    pass
