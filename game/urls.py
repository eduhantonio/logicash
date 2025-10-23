from django.contrib import admin # noqa: F401
from django.urls import path, include # noqa: F401
from . import views

urlpatterns = [
    # Página inicial
    path('', views.index, name='index'),
    path('', views.base, name='base'),
    
    # Principais Views
    path('dashboard/', views.dashboard_view, name='dashboard'), # Dashboard principal
    path('ranking/', views.ranking_view, name='ranking'),       # Página de ranking
    path('estatisticas/', views.estatisticas_view, name='estatisticas'), # Página de estatísticas
    path('profile/', views.profile_view, name='profile'), # Página de perfil do usuário
    path('desafios/', views.lista_desafios, name='desafios'), 
    
    # Autenticação
    path('login/', views.login_view, name='login'),
    path('signup/', views.signup_view, name='signup'),
    path('logout/', views.logout_view, name='logout'),
    
    # Redefinição de senha
    path('password-reset/', views.password_reset_view, name='password_reset'),
    path('password-reset/done/', views.password_reset_done_view, name='password_reset_done'),
    path('password-reset/confirm/<int:user_id>/<str:token>/', views.password_reset_confirm_view, name='password_reset_confirm'),   
]
