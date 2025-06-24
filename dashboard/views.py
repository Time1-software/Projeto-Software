from django.shortcuts import render
from django.contrib.auth.decorators import login_required
# Create your views here.

@login_required
def dashboard_home(request):

    context = {
        'nome_responsavel': request.user.first_name or request.user.username
    }
    
    return render(request, 'dashboard/index.html', context)