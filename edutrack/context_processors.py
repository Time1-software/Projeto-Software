from .models import Profile

def menu_context(request):
    if not request.user.is_authenticated:
        return {}

    perfil = getattr(request.user, 'profile', None)
    categoria = getattr(perfil, 'categoria', None)

    menu_items = []

    if categoria == 'aluno':
        menu_items = [
            {'nome': 'Página Inicial', 'url': 'painelAluno'},
            {'nome': 'Grade Horária', 'url': 'grade_aluno'},
            {'nome': 'Próximas Tarefas', 'url': 'tarefas'},
            {'nome': 'Boletim', 'url': 'boletim_escolar'},
           
        ]
    elif categoria == 'professor':
        menu_items = [
            {'nome': 'Minhas Turmas', 'url': '#'},
            {'nome': 'Lançar Notas', 'url': '#'},
        ]
    elif categoria == 'responsavel':
        menu_items = [
            {'nome': 'Desempenho Geral', 'url': '#'},
        ]

    return {'menu_items': menu_items}
