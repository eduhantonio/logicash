from django import forms
from django.contrib.auth.forms import UserCreationForm, AuthenticationForm, PasswordResetForm
from django.contrib.auth.models import User
from .models import Estudante


class LoginForm(AuthenticationForm):
    """
    Formulário de login customizado para o LogiCash
    """
    username = forms.CharField(
        max_length=150,
        widget=forms.TextInput(attrs={
            'class': 'form-control',
            'placeholder': 'Nome de usuário ou email',
            'autocomplete': 'username'
        }),
        label='Usuário'
    )
    password = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control',
            'placeholder': 'Digite sua senha',
            'autocomplete': 'current-password'
        }),
        label='Senha'
    )
    remember_me = forms.BooleanField(
        required=False,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Lembrar de mim'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        # Remover validação automática de username
        self.fields['username'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': 'Nome de usuário ou email',
            'required': True
        })
        self.fields['password'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': 'Digite sua senha',
            'required': True
        })


class SignupForm(UserCreationForm):
    """
    Formulário de cadastro customizado para o LogiCash
    """
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Digite seu email',
            'autocomplete': 'email'
        }),
        label='Email',
        help_text='Digite um email válido'
    )
    first_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Digite seu primeiro nome',
            'autocomplete': 'given-name'
        }),
        label='Primeiro Nome'
    )
    last_name = forms.CharField(
        max_length=30,
        widget=forms.TextInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Digite seu sobrenome',
            'autocomplete': 'family-name'
        }),
        label='Sobrenome'
    )
    escola = forms.CharField(
        max_length=200,
        widget=forms.TextInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Nome da sua escola',
            'autocomplete': 'organization'
        }),
        label='Escola',
        required=False
    )
    serie = forms.CharField(
        max_length=50,
        widget=forms.TextInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Ex: 8º Ano, 1º EM, etc.',
            'autocomplete': 'off'
        }),
        label='Série',
        required=False
    )
    data_nascimento = forms.DateField(
        widget=forms.DateInput(attrs={
            'class': 'form-control auth-input',
            'type': 'date',
            'autocomplete': 'bday'
        }),
        label='Data de Nascimento',
        required=False
    )
    aceito_termos = forms.BooleanField(
        required=True,
        widget=forms.CheckboxInput(attrs={
            'class': 'form-check-input'
        }),
        label='Aceito os termos de uso e política de privacidade'
    )

    class Meta:
        model = User
        fields = ('username', 'email', 'first_name', 'last_name', 'password1', 'password2')

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        
        # Customizar campos de senha
        self.fields['username'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': 'Escolha um nome de usuário',
            'autocomplete': 'username'
        })
        self.fields['password1'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': 'Digite uma senha segura',
            'autocomplete': 'new-password'
        })
        self.fields['password2'].widget.attrs.update({
            'class': 'form-control auth-input',
            'placeholder': 'Confirme sua senha',
            'autocomplete': 'new-password'
        })
        
        # Remover help_text dos campos de senha
        self.fields['password1'].help_text = None
        self.fields['password2'].help_text = None
        
        # Adicionar ajuda visual para senha
        self.fields['password1'].help_text = (
            'Sua senha deve ter pelo menos 8 caracteres e não pode ser muito comum.'
        )

    def clean_email(self):
        email = self.cleaned_data.get('email')
        if User.objects.filter(email=email).exists():
            raise forms.ValidationError('Este email já está sendo usado.')
        return email

    def clean_username(self):
        username = self.cleaned_data.get('username')
        if len(username) < 3:
            raise forms.ValidationError('O nome de usuário deve ter pelo menos 3 caracteres.')
        return username

    def save(self, commit=True):
        user = super().save(commit=False)
        user.email = self.cleaned_data['email']
        user.first_name = self.cleaned_data['first_name']
        user.last_name = self.cleaned_data['last_name']
        
        if commit:
            user.save()
            
            # Criar perfil do estudante
            Estudante.objects.create(
                user=user,
                nome=f"{user.first_name} {user.last_name}".strip(),
                escola=self.cleaned_data.get('escola', ''),
                serie=self.cleaned_data.get('serie', ''),
                data_nascimento=self.cleaned_data.get('data_nascimento')
            )
            
        return user


class PasswordResetFormCustom(PasswordResetForm):
    """
    Formulário de redefinição de senha customizado
    """
    email = forms.EmailField(
        max_length=254,
        widget=forms.EmailInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Digite seu email cadastrado',
            'autocomplete': 'email'
        }),
        label='Email'
    )

    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.fields['email'].help_text = (
            'Digite o email associado à sua conta. '
            'Enviaremos instruções para redefinir sua senha.'
        )


class SetPasswordForm(forms.Form):
    """
    Formulário para definir nova senha
    """
    new_password1 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Digite sua nova senha',
            'autocomplete': 'new-password'
        }),
        label='Nova Senha'
    )
    new_password2 = forms.CharField(
        widget=forms.PasswordInput(attrs={
            'class': 'form-control auth-input',
            'placeholder': 'Confirme sua nova senha',
            'autocomplete': 'new-password'
        }),
        label='Confirmar Nova Senha'
    )

    def __init__(self, user, *args, **kwargs):
        self.user = user
        super().__init__(*args, **kwargs)

    def clean_new_password2(self):
        password1 = self.cleaned_data.get('new_password1')
        password2 = self.cleaned_data.get('new_password2')
        
        if password1 and password2:
            if password1 != password2:
                raise forms.ValidationError('As senhas não coincidem.')
            if len(password1) < 8:
                raise forms.ValidationError('A senha deve ter pelo menos 8 caracteres.')
        
        return password2

    def save(self, commit=True):
        password = self.cleaned_data['new_password1']
        self.user.set_password(password)
        if commit:
            self.user.save()
        return self.user


class ProfileUpdateForm(forms.ModelForm):
    """
    Formulário para atualização do perfil do estudante
    """
    class Meta:
        model = Estudante
        fields = ['nome', 'escola', 'serie', 'data_nascimento']
        widgets = {
            'nome': forms.TextInput(attrs={
                'class': 'form-control auth-input',
                'placeholder': 'Nome completo'
            }),
            'escola': forms.TextInput(attrs={
                'class': 'form-control auth-input',
                'placeholder': 'Nome da escola'
            }),
            'serie': forms.TextInput(attrs={
                'class': 'form-control auth-input',
                'placeholder': 'Série atual'
            }),
            'data_nascimento': forms.DateInput(attrs={
                'class': 'form-control auth-input',
                'type': 'date'
            }),
        }
        labels = {
            'nome': 'Nome Completo',
            'escola': 'Escola',
            'serie': 'Série',
            'data_nascimento': 'Data de Nascimento',
        }
