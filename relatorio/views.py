from django.shortcuts import render
from .models import RelatorioProducao
from .models import RelatorioFuncionario


def relatorio_funcionario(request):
    relatorios = RelatorioFuncionario.objects.all()
    context = {"relatorios": relatorios}
    return render(request, "relatorio_funcionario.html", context)


def relatorio_producao(request):
    relatorios = RelatorioProducao.objects.all()
    context = {"relatorios": relatorios}
    return render(request, "relatorio_producao.html", context)
