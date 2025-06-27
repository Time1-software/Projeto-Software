from django.shortcuts import render

def professor(request):
    return render(request, 'professor.html')

def painel_turmas(request):
    return render(request, 'painel_turmas.html')

def resumo(request):
    return render(request, 'resumo.html')