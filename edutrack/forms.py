from django import forms
from .models import Aluno,Tarefa, Turma
from django.contrib.auth.forms import AuthenticationForm, UserCreationForm
from django.contrib.auth import authenticate
from django.contrib.auth.models import User
from .models import Profile, CATEGORIAS

class AlunoForm(forms.ModelForm):
    class Meta:
        model = Aluno
        fields = [
            'nome', 'matricula', 'turma',
            'pontualidade', 'participacao_aula', 'entregas_tarefas',
            'comportamento_funcionarios', 'participacao_oficinas',
            'comportamento_sala', 'participacao_plataformas'
        ]
        widgets = {
            'nome': forms.TextInput(attrs={'placeholder': 'Nome completo'}),
            'matricula': forms.TextInput(attrs={'placeholder': 'Ex: 2025.1'}),
            'turma': forms.TextInput(attrs={'placeholder': 'Turma / Curso'}),
            # campos numéricos
            'pontualidade': forms.NumberInput(attrs={'min':0, 'max':100}),
            'participacao_aula': forms.NumberInput(attrs={'min':0, 'max':100}),
            'entregas_tarefas': forms.NumberInput(attrs={'min':0, 'max':100}),
            'comportamento_funcionarios': forms.NumberInput(attrs={'min':0, 'max':100}),
            'participacao_oficinas': forms.NumberInput(attrs={'min':0, 'max':100}),
            'comportamento_sala': forms.NumberInput(attrs={'min':0, 'max':100}),
            'participacao_plataformas': forms.NumberInput(attrs={'min':0, 'max':100}),
        }
        labels = {
            'pontualidade': 'Pontualidade (%)',
            'participacao_aula': 'Participação em aula (%)',
            'entregas_tarefas': 'Entregas de tarefas (%)',
            'comportamento_funcionarios': 'Comportamento c/ funcionários (%)',
            'participacao_oficinas': 'Participação em oficinas (%)',
            'comportamento_sala': 'Comportamento em sala (%)',
            'participacao_plataformas': 'Participação em plataformas (%)',
        }

#LOGIN

class CustomLoginForm(AuthenticationForm):
    username = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'placeholder':'seu_email@exemplo.com','class':'input-text'}),
    )
    password = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder':'••••••','class':'input-text'}),
    )
    categoria = forms.ChoiceField(
        choices=CATEGORIAS,
        widget=forms.RadioSelect(attrs={'class':'radio-group'}),
        label='Tipo de conta'
    )

    def clean(self):
        cleaned = super().clean()
        email = cleaned.get('username')
        senha = cleaned.get('password')
        categoria = cleaned.get('categoria')

        # 1) Existe ao menos um usuário com esse e-mail?
        if not User.objects.filter(username=email).exists():
            raise forms.ValidationError("Este e-mail não está cadastrado.")

        # 2) Autentica (username=email, password)
        user = authenticate(username=email, password=senha)
        if user is None:
            # Se há usuário(s) com esse e-mail, mas authenticate falhou:
            raise forms.ValidationError("Senha incorreta.")

        # 3) Verifica categoria via Profile
        try:
            profile = Profile.objects.get(user=user)
        except Profile.DoesNotExist:
            raise forms.ValidationError("Perfil de usuário não encontrado.")
        if profile.categoria != categoria:
            raise forms.ValidationError("Tipo de conta incorreto.")

        # 4) Finalmente, autoriza o login
        self.confirm_login_allowed(user)
        return cleaned

class CustomSignupForm(UserCreationForm):
    email = forms.EmailField(
        label='E-mail',
        widget=forms.EmailInput(attrs={'placeholder':'seu_email@exemplo.com','class':'input-text'}),
    )
    categoria = forms.ChoiceField(
        choices=CATEGORIAS,
        widget=forms.RadioSelect(attrs={'class':'radio-group'}),
        label='Categoria'
    )
    password1 = forms.CharField(
        label='Senha',
        widget=forms.PasswordInput(attrs={'placeholder':'••••••','class':'input-text'}),
    )
    password2 = forms.CharField(
        label='Confirmação de senha',
        widget=forms.PasswordInput(attrs={'placeholder':'••••••','class':'input-text'}),
    )

    class Meta:
        model = User
        fields = ('email','categoria','password1','password2')

    def clean_email(self):
        email = self.cleaned_data.get('email')
        # Valida formato de e-mail por EmailField
        # Valida unicidade:
        if User.objects.filter(username=email).exists():
            raise forms.ValidationError("Já existe uma conta com este e-mail.")
        return email

    def save(self, commit=True):
        # Aqui o username será igual ao email
        user = User(username=self.cleaned_data['email'], email=self.cleaned_data['email'])
        user.set_password(self.cleaned_data['password1'])
        if commit:
            user.save()
            Profile.objects.create(
                user=user,
                categoria=self.cleaned_data['categoria']
            )
        return user

class TarefaForm(forms.ModelForm):
    tipo = forms.ChoiceField(choices=Tarefa.TipoTarefa.choices, label="Tipo da Tarefa")

    turma = forms.ModelChoiceField(
        queryset=Turma.objects.all(),
        label="Turma"
    )

    class Meta:
        model = Tarefa
        fields = ['titulo', 'data', 'tipo', 'descricao', 'turma']
        widgets = {
            'data': forms.DateInput(attrs={'type': 'date'}),
        }
