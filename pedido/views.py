from django.shortcuts import render
from django.views.generic import ListView
from django.views.generic import DetailView
from django.views import View
from . import models


class ListaPedido(ListView):
    model = models.Pedido


class DetalhePedido(DetailView):
    pass


class CriaPedido(View):
    pass


class EditaPedido(View):
    pass
