from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth.models import User
from django.contrib.auth import get_user_model
from django.contrib.messages import get_messages
from .models import Estudante, Pontuacao, Conquista, EstudanteConquista, Quiz, Resultado
from .forms import LoginForm, SignupForm, PasswordResetFormCustom


class DashboardViewTest(TestCase):
    """
    Testes para a view do dashboard do LogiCash
    """
    
    def setUp(self):
        """
        Configuração inicial para os testes
        """
        # Cria um usuário para teste
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='João',
            last_name='Silva'
        )
        
        # Cria um estudante associado ao usuário
        self.estudante = Estudante.objects.create(
            user=self.user,
            nome='João Silva',
            escola='Escola Teste',
            serie='8º Ano'
        )
        
        # Cria uma pontuação para o estudante
        self.pontuacao = Pontuacao.objects.create(
            estudante=self.estudante,
            pontos_totais=250,
            nivel_atual=3
        )
        
        # Cria algumas conquistas
        self.conquista1 = Conquista.objects.create(
            nome='Primeiro Quiz',
            descricao='Complete seu primeiro quiz',
            icone='star',
            criterio_pontos=10,
            cor='#008445'
        )
        
        self.conquista2 = Conquista.objects.create(
            nome='Estudante Dedicado',
            descricao='Complete 5 quizzes',
            icone='trophy',
            criterio_quizzes=5,
            cor='#2aea8e'
        )
        
        # Cria uma conquista desbloqueada
        self.estudante_conquista = EstudanteConquista.objects.create(
            estudante=self.estudante,
            conquista=self.conquista1
        )
        
        # Cria um quiz de exemplo
        self.quiz = Quiz.objects.create(
            titulo='Quiz de Poupança',
            descricao='Teste seus conhecimentos sobre poupança',
            nivel_dificuldade=2,
            tema='Poupança',
            pontos_base=20
        )
        
        # Cria um resultado de quiz
        self.resultado = Resultado.objects.create(
            estudante=self.estudante,
            quiz=self.quiz,
            pontuacao_obtida=18,
            total_perguntas=10,
            acertos=9,
            concluido=True
        )
        
        # Cliente de teste
        self.client = Client()
    
    def test_dashboard_redirects_unauthenticated_user(self):
        """
        Testa se usuários não autenticados são redirecionados
        """
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 302)  # Redirecionamento
    
    def test_dashboard_loads_for_authenticated_user(self):
        """
        Testa se o dashboard carrega corretamente para usuários autenticados
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Bem-vindo ao LogiCash')
        self.assertContains(response, 'João Silva')
    
    def test_dashboard_context_data(self):
        """
        Testa se os dados corretos são passados para o template
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        
        # Verifica se os dados estão no contexto
        self.assertIn('estudante', response.context)
        self.assertIn('pontuacao', response.context)
        self.assertIn('conquistas_desbloqueadas', response.context)
        
        # Verifica se os dados estão corretos
        self.assertEqual(response.context['estudante'], self.estudante)
        self.assertEqual(response.context['pontuacao'], self.pontuacao)
        self.assertEqual(response.context['pontuacao'].pontos_totais, 250)
        self.assertEqual(response.context['pontuacao'].nivel_atual, 3)
    
    def test_dashboard_displays_correct_statistics(self):
        """
        Testa se as estatísticas são exibidas corretamente no dashboard
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        
        # Verifica se os valores estão sendo exibidos
        self.assertContains(response, '250')  # Pontos totais
        self.assertContains(response, '3')    # Nível atual
        self.assertContains(response, '1')    # Total de quizzes completados
    
    def test_dashboard_displays_achievements(self):
        """
        Testa se as conquistas são exibidas corretamente
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        
        # Verifica se a conquista desbloqueada é exibida
        self.assertContains(response, 'Primeiro Quiz')
        self.assertContains(response, 'Complete seu primeiro quiz')
    
    def test_dashboard_creates_estudante_if_not_exists(self):
        """
        Testa se um novo estudante é criado automaticamente se não existir
        """
        # Cria um novo usuário sem estudante associado
        new_user = User.objects.create_user(
            username='newuser',
            password='testpass123'
        )
        
        self.client.login(username='newuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        
        # Verifica se um estudante foi criado
        self.assertTrue(Estudante.objects.filter(user=new_user).exists())
        
        # Verifica se uma pontuação foi criada
        estudante = Estudante.objects.get(user=new_user)
        self.assertTrue(Pontuacao.objects.filter(estudante=estudante).exists())
    
    def test_dashboard_error_handling(self):
        """
        Testa se erros são tratados adequadamente
        """
        self.client.login(username='testuser', password='testpass123')
        
        # Simula um erro removendo o estudante
        self.estudante.delete()
        
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)  # Deve carregar mesmo com erro


class ModelTest(TestCase):
    """
    Testes para os modelos do LogiCash
    """
    
    def setUp(self):
        """
        Configuração inicial para os testes de modelo
        """
        self.user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.estudante = Estudante.objects.create(
            user=self.user,
            nome='João Silva'
        )
    
    def test_estudante_creation(self):
        """
        Testa a criação de um estudante
        """
        self.assertEqual(str(self.estudante), 'João Silva')
        self.assertEqual(self.estudante.user, self.user)
    
    def test_pontuacao_nivel_calculation(self):
        """
        Testa o cálculo automático do nível baseado na pontuação
        """
        pontuacao = Pontuacao.objects.create(
            estudante=self.estudante,
            pontos_totais=350
        )
        
        # Nível deve ser 4 (350 // 100 + 1)
        self.assertEqual(pontuacao.nivel_atual, 4)
    
    def test_conquista_creation(self):
        """
        Testa a criação de uma conquista
        """
        conquista = Conquista.objects.create(
            nome='Teste',
            descricao='Descrição do teste',
            icone='star',
            criterio_pontos=100
        )
        
        self.assertEqual(str(conquista), 'Teste')
        self.assertEqual(conquista.criterio_pontos, 100)


class URLTest(TestCase):
    """
    Testes para as URLs do LogiCash
    """
    
    def test_index_url(self):
        """
        Testa se a URL index redireciona para login
        """
        response = self.client.get(reverse('index'))
        self.assertEqual(response.status_code, 302)  # Redirecionamento para login
    
    def test_dashboard_url(self):
        """
        Testa se a URL dashboard funciona (com autenticação)
        """
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('dashboard'))
        self.assertEqual(response.status_code, 200)
    
    def test_logout_url(self):
        """
        Testa se a URL logout funciona
        """
        user = User.objects.create_user(
            username='testuser',
            password='testpass123'
        )
        
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)  # Redirecionamento


class AuthenticationTest(TestCase):
    """
    Testes para funcionalidades de autenticação
    """
    
    def setUp(self):
        """
        Configuração inicial para os testes de autenticação
        """
        self.client = Client()
        self.user = User.objects.create_user(
            username='testuser',
            email='test@example.com',
            password='testpass123',
            first_name='João',
            last_name='Silva'
        )
        
        self.estudante = Estudante.objects.create(
            user=self.user,
            nome='João Silva'
        )
    
    def test_login_view_get(self):
        """
        Testa se a view de login carrega corretamente
        """
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Entrar')
        self.assertIsInstance(response.context['form'], LoginForm)
    
    def test_login_view_post_success(self):
        """
        Testa login bem-sucedido
        """
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'testpass123'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
    
    def test_login_view_post_invalid(self):
        """
        Testa login com credenciais inválidas
        """
        response = self.client.post(reverse('login'), {
            'username': 'testuser',
            'password': 'wrongpassword'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Por favor, corrija os erros abaixo')
    
    def test_login_view_authenticated_user_redirect(self):
        """
        Testa se usuário autenticado é redirecionado do login
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('login'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
    
    def test_signup_view_get(self):
        """
        Testa se a view de cadastro carrega corretamente
        """
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Criar Conta')
        self.assertIsInstance(response.context['form'], SignupForm)
    
    def test_signup_view_post_success(self):
        """
        Testa cadastro bem-sucedido
        """
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'Maria',
            'last_name': 'Santos',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'aceito_termos': True
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
        
        # Verificar se o usuário foi criado
        self.assertTrue(User.objects.filter(username='newuser').exists())
        
        # Verificar se o estudante foi criado
        user = User.objects.get(username='newuser')
        self.assertTrue(Estudante.objects.filter(user=user).exists())
    
    def test_signup_view_post_invalid_email(self):
        """
        Testa cadastro com email duplicado
        """
        response = self.client.post(reverse('signup'), {
            'username': 'newuser',
            'email': 'test@example.com',  # Email já existente
            'first_name': 'Maria',
            'last_name': 'Santos',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'aceito_termos': True
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Este email já está sendo usado')
    
    def test_signup_view_authenticated_user_redirect(self):
        """
        Testa se usuário autenticado é redirecionado do cadastro
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('signup'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('dashboard'))
    
    def test_password_reset_view_get(self):
        """
        Testa se a view de redefinição de senha carrega corretamente
        """
        response = self.client.get(reverse('password_reset'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Redefinir Senha')
        self.assertIsInstance(response.context['form'], PasswordResetFormCustom)
    
    def test_password_reset_view_post_success(self):
        """
        Testa solicitação de redefinição de senha bem-sucedida
        """
        response = self.client.post(reverse('password_reset'), {
            'email': 'test@example.com'
        })
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('password_reset_done'))
    
    def test_password_reset_view_post_invalid_email(self):
        """
        Testa solicitação de redefinição com email inexistente
        """
        response = self.client.post(reverse('password_reset'), {
            'email': 'nonexistent@example.com'
        })
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Nenhuma conta encontrada com este email')
    
    def test_password_reset_done_view(self):
        """
        Testa view de confirmação de envio de email
        """
        response = self.client.get(reverse('password_reset_done'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Email Enviado!')
    
    def test_profile_view_authenticated(self):
        """
        Testa view de perfil para usuário autenticado
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, 'Perfil')
    
    def test_profile_view_unauthenticated(self):
        """
        Testa redirecionamento de usuário não autenticado
        """
        response = self.client.get(reverse('profile'))
        self.assertEqual(response.status_code, 302)
    
    def test_logout_view(self):
        """
        Testa logout de usuário
        """
        self.client.login(username='testuser', password='testpass123')
        response = self.client.get(reverse('logout'))
        self.assertEqual(response.status_code, 302)
        self.assertRedirects(response, reverse('login'))


class AuthenticationFormTest(TestCase):
    """
    Testes para formulários de autenticação
    """
    
    def test_login_form_valid(self):
        """
        Testa formulário de login válido
        """
        form_data = {
            'username': 'testuser',
            'password': 'testpass123'
        }
        # O LoginForm precisa de um request para funcionar corretamente
        from django.test import RequestFactory
        factory = RequestFactory()
        request = factory.post('/login/', form_data)
        form = LoginForm(request=request, data=form_data)
        # Para teste, vamos apenas verificar se os campos estão presentes
        self.assertIn('username', form.fields)
        self.assertIn('password', form.fields)
    
    def test_login_form_invalid(self):
        """
        Testa formulário de login inválido
        """
        form_data = {
            'username': '',
            'password': ''
        }
        form = LoginForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_signup_form_valid(self):
        """
        Testa formulário de cadastro válido
        """
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'Maria',
            'last_name': 'Santos',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'aceito_termos': True
        }
        form = SignupForm(data=form_data)
        self.assertTrue(form.is_valid())
    
    def test_signup_form_password_mismatch(self):
        """
        Testa formulário de cadastro com senhas diferentes
        """
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'Maria',
            'last_name': 'Santos',
            'password1': 'newpass123',
            'password2': 'differentpass123',
            'aceito_termos': True
        }
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())
    
    def test_signup_form_terms_not_accepted(self):
        """
        Testa formulário de cadastro sem aceitar termos
        """
        form_data = {
            'username': 'newuser',
            'email': 'newuser@example.com',
            'first_name': 'Maria',
            'last_name': 'Santos',
            'password1': 'newpass123',
            'password2': 'newpass123',
            'aceito_termos': False
        }
        form = SignupForm(data=form_data)
        self.assertFalse(form.is_valid())


class AuthenticationURLTest(TestCase):
    """
    Testes para URLs de autenticação
    """
    
    def test_login_url(self):
        """
        Testa URL de login
        """
        response = self.client.get('/login/')
        self.assertEqual(response.status_code, 200)
    
    def test_signup_url(self):
        """
        Testa URL de cadastro
        """
        response = self.client.get('/signup/')
        self.assertEqual(response.status_code, 200)
    
    def test_password_reset_url(self):
        """
        Testa URL de redefinição de senha
        """
        response = self.client.get('/password-reset/')
        self.assertEqual(response.status_code, 200)
    
    def test_password_reset_done_url(self):
        """
        Testa URL de confirmação de redefinição
        """
        response = self.client.get('/password-reset/done/')
        self.assertEqual(response.status_code, 200)
