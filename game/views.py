from django.shortcuts import render, redirect, get_object_or_404
from django.http import HttpResponse, JsonResponse
from django.contrib.auth.decorators import login_required
from django.contrib.auth import logout, login, authenticate
from django.contrib.auth.models import User
from django.contrib import messages
from django.db.models import Count, Sum
from django.core.mail import send_mail
from django.conf import settings
from django.utils.crypto import get_random_string
from django.utils import timezone
from django.urls import reverse
from .models import Estudante, Pontuacao, Conquista, EstudanteConquista, Resultado
from .forms import LoginForm, SignupForm, PasswordResetFormCustom, SetPasswordForm, ProfileUpdateForm


def index(request):
    """
    View principal - redireciona para dashboard se autenticado, senão para login
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    return redirect('login')


@login_required
def dashboard_view(request):
    """
    View do dashboard do estudante - exibe pontuação, conquistas e progresso
    """
    try:
        # Busca ou cria o perfil do estudante
        estudante, created = Estudante.objects.get_or_create(
            user=request.user,
            defaults={'nome': request.user.get_full_name() or request.user.username}
        )
        
        # Busca ou cria a pontuação do estudante
        pontuacao, created = Pontuacao.objects.get_or_create(
            estudante=estudante,
            defaults={'pontos_totais': 0, 'nivel_atual': 1}
        )
        
        # Busca conquistas desbloqueadas pelo estudante
        conquistas_desbloqueadas = EstudanteConquista.objects.filter(
            estudante=estudante
        ).select_related('conquista').order_by('-data_desbloqueio')[:6]
        
        # Busca estatísticas adicionais
        total_quizzes = Resultado.objects.filter(estudante=estudante, concluido=True).count()
        total_acertos = Resultado.objects.filter(estudante=estudante).aggregate(
            total=Sum('acertos')
        )['total'] or 0
        total_perguntas = Resultado.objects.filter(estudante=estudante).aggregate(
            total=Sum('total_perguntas')
        )['total'] or 0
        
        # Calcula percentual de acertos
        percentual_acertos = (total_acertos / total_perguntas * 100) if total_perguntas > 0 else 0
        
        # Busca conquistas disponíveis para mostrar próximas metas
        conquistas_disponiveis = Conquista.objects.filter(ativa=True).exclude(
            estudantes__estudante=estudante
        ).order_by('criterio_pontos')[:3]
        
        # Dados para o gráfico de progresso (últimos 7 resultados)
        resultados_recentes = Resultado.objects.filter(
            estudante=estudante, 
            concluido=True
        ).order_by('-data_realizacao')[:7]
        
        context = {
            'estudante': estudante,
            'pontuacao': pontuacao,
            'conquistas_desbloqueadas': conquistas_desbloqueadas,
            'conquistas_disponiveis': conquistas_disponiveis,
            'total_quizzes': total_quizzes,
            'total_acertos': total_acertos,
            'total_perguntas': total_perguntas,
            'percentual_acertos': round(percentual_acertos, 1),
            'resultados_recentes': resultados_recentes,
        }
        
        return render(request, 'index.html', context)
        
    except Exception as e:
        messages.error(request, f"Erro ao carregar dashboard: {str(e)}")
        return render(request, 'index.html', {
            'estudante': None,
            'pontuacao': None,
            'conquistas_desbloqueadas': [],
            'conquistas_disponiveis': [],
            'total_quizzes': 0,
            'total_acertos': 0,
            'total_perguntas': 0,
            'percentual_acertos': 0,
            'resultados_recentes': [],
        })


def logout_view(request):
    """
    View para logout do usuário
    """
    logout(request)
    messages.success(request, "Logout realizado com sucesso!")
    return redirect('login')


# ==================== VIEWS DE AUTENTICAÇÃO ====================

def login_view(request):
    """
    View para login de usuários
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = LoginForm(request, data=request.POST)
        if form.is_valid():
            username = form.cleaned_data.get('username')
            password = form.cleaned_data.get('password')
            remember_me = form.cleaned_data.get('remember_me', False)
            
            # Tentar autenticar por username ou email
            user = authenticate(request, username=username, password=password)
            if user is None:
                # Tentar buscar por email
                try:
                    user_by_email = User.objects.get(email=username)
                    user = authenticate(request, username=user_by_email.username, password=password)
                except User.DoesNotExist:
                    pass
            
            if user is not None:
                login(request, user)
                
                # Configurar sessão baseado em "lembrar de mim"
                if not remember_me:
                    request.session.set_expiry(0)  # Sessão expira quando o navegador fecha
                else:
                    request.session.set_expiry(1209600)  # 2 semanas
                
                messages.success(request, f"Bem-vindo de volta, {user.first_name or user.username}!")
                
                # Redirecionar para a próxima página ou dashboard
                next_page = request.GET.get('next', 'dashboard')
                return redirect(next_page)
            else:
                messages.error(request, "Usuário ou senha incorretos.")
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = LoginForm()
    
    return render(request, 'auth/login.html', {'form': form})


def signup_view(request):
    """
    View para cadastro de novos usuários
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = SignupForm(request.POST)
        if form.is_valid():
            user = form.save()
            
            # Criar pontuação inicial para o estudante
            try:
                estudante = Estudante.objects.get(user=user)
                Pontuacao.objects.get_or_create(
                    estudante=estudante,
                    defaults={'pontos_totais': 0, 'nivel_atual': 1}
                )
            except Estudante.DoesNotExist:
                pass
            
            # Logar o usuário automaticamente
            login(request, user)
            messages.success(request, f"Conta criada com sucesso! Bem-vindo ao LogiCash, {user.first_name}!")
            return redirect('dashboard')
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = SignupForm()
    
    return render(request, 'auth/signup.html', {'form': form})


def password_reset_view(request):
    """
    View para solicitação de redefinição de senha
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    if request.method == 'POST':
        form = PasswordResetFormCustom(request.POST)
        if form.is_valid():
            email = form.cleaned_data['email']
            
            try:
                user = User.objects.get(email=email)
                
                # Gerar token temporário (em produção, use uma solução mais robusta)
                token = get_random_string(32)
                request.session[f'reset_token_{user.id}'] = {
                    'token': token,
                    'timestamp': timezone.now().isoformat()
                }
                
                # Em produção, enviar email aqui
                # send_mail(
                #     'Redefinição de Senha - LogiCash',
                #     f'Use este link para redefinir sua senha: {request.build_absolute_uri(reverse("password_reset_confirm", args=[user.id, token]))}',
                #     settings.DEFAULT_FROM_EMAIL,
                #     [email],
                #     fail_silently=False,
                # )
                
                messages.success(request, 
                    f"Instruções para redefinir sua senha foram enviadas para {email}. "
                    f"Em desenvolvimento, use o token: {token}"
                )
                return redirect('password_reset_done')
                
            except User.DoesNotExist:
                messages.error(request, "Nenhuma conta encontrada com este email.")
        else:
            messages.error(request, "Por favor, digite um email válido.")
    else:
        form = PasswordResetFormCustom()
    
    return render(request, 'auth/password_reset.html', {'form': form})


def password_reset_done_view(request):
    """
    View para confirmar envio do email de redefinição
    """
    return render(request, 'auth/password_reset_done.html')


def password_reset_confirm_view(request, user_id, token):
    """
    View para confirmar redefinição de senha
    """
    if request.user.is_authenticated:
        return redirect('dashboard')
    
    try:
        user = User.objects.get(id=user_id)
        session_key = f'reset_token_{user_id}'
        
        if session_key not in request.session:
            messages.error(request, "Token inválido ou expirado.")
            return redirect('password_reset')
        
        stored_data = request.session[session_key]
        if stored_data['token'] != token:
            messages.error(request, "Token inválido.")
            return redirect('password_reset')
        
        # Verificar se o token não expirou (24 horas)
        from datetime import datetime, timedelta
        token_time = datetime.fromisoformat(stored_data['timestamp'])
        if timezone.now() - token_time.replace(tzinfo=timezone.utc) > timedelta(hours=24):
            del request.session[session_key]
            messages.error(request, "Token expirado. Solicite um novo.")
            return redirect('password_reset')
        
        if request.method == 'POST':
            form = SetPasswordForm(user, request.POST)
            if form.is_valid():
                form.save()
                del request.session[session_key]
                messages.success(request, "Senha redefinida com sucesso! Faça login com sua nova senha.")
                return redirect('login')
            else:
                messages.error(request, "Por favor, corrija os erros abaixo.")
        else:
            form = SetPasswordForm(user)
        
        return render(request, 'auth/password_reset_confirm.html', {
            'form': form,
            'user': user
        })
        
    except User.DoesNotExist:
        messages.error(request, "Usuário não encontrado.")
        return redirect('password_reset')


@login_required
def profile_view(request):
    """
    View para visualizar e editar perfil do usuário
    """
    try:
        estudante = request.user.estudante
    except Estudante.DoesNotExist:
        # Criar perfil se não existir
        estudante = Estudante.objects.create(
            user=request.user,
            nome=request.user.get_full_name() or request.user.username
        )
    
    if request.method == 'POST':
        form = ProfileUpdateForm(request.POST, instance=estudante)
        if form.is_valid():
            form.save()
            messages.success(request, "Perfil atualizado com sucesso!")
            return redirect('profile')
        else:
            messages.error(request, "Por favor, corrija os erros abaixo.")
    else:
        form = ProfileUpdateForm(instance=estudante)
    
    context = {
        'estudante': estudante,
        'form': form,
        'pontuacao': getattr(estudante, 'pontuacao', None)
    }
    
    return render(request, 'auth/profile.html', context)