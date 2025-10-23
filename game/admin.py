from django.contrib import admin
from django.contrib.auth.admin import UserAdmin
from django.contrib.auth.models import User
from .models import (
    Estudante, Pontuacao, Conquista, EstudanteConquista, 
    Quiz, Pergunta, Resposta, Resultado, Modulo, Desafio, ProgressoDesafio
)


class EstudanteInline(admin.StackedInline):
    """
    Inline para exibir dados do estudante no admin do usuário
    """
    model = Estudante
    can_delete = False
    verbose_name_plural = 'Dados do Estudante'
    fields = ('nome', 'data_nascimento', 'escola', 'serie', 'avatar')


class CustomUserAdmin(UserAdmin):
    """
    Admin customizado para usuários com dados do estudante
    """
    inlines = (EstudanteInline,)
    list_display = ('username', 'email', 'first_name', 'last_name', 'is_staff', 'get_estudante_nome')
    list_filter = ('is_staff', 'is_superuser', 'is_active', 'date_joined')
    
    def get_estudante_nome(self, obj):
        """Retorna o nome do estudante se existir"""
        try:
            return obj.estudante.nome
        except:
            return "Não definido"
    get_estudante_nome.short_description = 'Nome do Estudante'


@admin.register(Estudante)
class EstudanteAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Estudante
    """
    list_display = ('nome', 'user', 'escola', 'serie', 'data_cadastro')
    list_filter = ('escola', 'serie', 'data_cadastro')
    search_fields = ('nome', 'user__username', 'user__email', 'escola')
    readonly_fields = ('data_cadastro',)
    fieldsets = (
        ('Informações Pessoais', {
            'fields': ('user', 'nome', 'data_nascimento', 'avatar')
        }),
        ('Informações Acadêmicas', {
            'fields': ('escola', 'serie')
        }),
        ('Dados do Sistema', {
            'fields': ('data_cadastro',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Pontuacao)
class PontuacaoAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Pontuacao
    """
    list_display = ('estudante', 'pontos_totais', 'nivel_atual', 'data_atualizacao')
    list_filter = ('nivel_atual', 'data_atualizacao')
    search_fields = ('estudante__nome', 'estudante__user__username')
    readonly_fields = ('data_atualizacao',)
    ordering = ('-pontos_totais',)


@admin.register(Conquista)
class ConquistaAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Conquista
    """
    list_display = ('nome', 'criterio_pontos', 'criterio_quizzes', 'ativa', 'cor')
    list_filter = ('ativa', 'criterio_pontos', 'criterio_quizzes')
    search_fields = ('nome', 'descricao')
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('nome', 'descricao', 'ativa')
        }),
        ('Aparência', {
            'fields': ('icone', 'icone_url', 'cor')
        }),
        ('Critérios de Desbloqueio', {
            'fields': ('criterio_pontos', 'criterio_quizzes', 'criterio_acertos', 'nivel_dificuldade'),
            'description': 'Pelo menos um critério deve ser definido para a conquista ser desbloqueada.'
        }),
    )


@admin.register(EstudanteConquista)
class EstudanteConquistaAdmin(admin.ModelAdmin):
    """
    Admin para o modelo EstudanteConquista
    """
    list_display = ('estudante', 'conquista', 'data_desbloqueio')
    list_filter = ('conquista', 'data_desbloqueio')
    search_fields = ('estudante__nome', 'conquista__nome')
    readonly_fields = ('data_desbloqueio',)
    ordering = ('-data_desbloqueio',)


class RespostaInline(admin.TabularInline):
    """
    Inline para exibir respostas de uma pergunta
    """
    model = Resposta
    extra = 4
    fields = ('texto', 'correta', 'ordem')


@admin.register(Pergunta)
class PerguntaAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Pergunta
    """
    list_display = ('texto_curto', 'quiz', 'ordem', 'pontos')
    list_filter = ('quiz', 'ordem')
    search_fields = ('texto', 'quiz__titulo')
    inlines = [RespostaInline]
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('quiz', 'texto', 'explicacao')
        }),
        ('Configurações', {
            'fields': ('ordem', 'pontos')
        }),
    )
    
    def texto_curto(self, obj):
        """Retorna uma versão curta do texto da pergunta"""
        return obj.texto[:50] + "..." if len(obj.texto) > 50 else obj.texto
    texto_curto.short_description = 'Pergunta'


class PerguntaInline(admin.TabularInline):
    """
    Inline para exibir perguntas de um quiz
    """
    model = Pergunta
    extra = 1
    fields = ('texto_curto', 'ordem', 'pontos')
    readonly_fields = ('texto_curto',)
    
    def texto_curto(self, obj):
        """Retorna uma versão curta do texto da pergunta"""
        if obj.pk:
            return obj.texto[:30] + "..." if len(obj.texto) > 30 else obj.texto
        return "Nova pergunta"
    texto_curto.short_description = 'Pergunta'


@admin.register(Quiz)
class QuizAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Quiz
    """
    list_display = ('titulo', 'tema', 'nivel_dificuldade', 'pontos_base', 'ativo', 'data_criacao')
    list_filter = ('nivel_dificuldade', 'tema', 'ativo', 'data_criacao')
    search_fields = ('titulo', 'descricao', 'tema')
    inlines = [PerguntaInline]
    readonly_fields = ('data_criacao',)
    fieldsets = (
        ('Informações Básicas', {
            'fields': ('titulo', 'descricao', 'tema', 'ativo')
        }),
        ('Configurações', {
            'fields': ('nivel_dificuldade', 'pontos_base', 'tempo_limite')
        }),
        ('Dados do Sistema', {
            'fields': ('data_criacao',),
            'classes': ('collapse',)
        }),
    )


@admin.register(Resultado)
class ResultadoAdmin(admin.ModelAdmin):
    """
    Admin para o modelo Resultado
    """
    list_display = ('estudante', 'quiz', 'acertos', 'total_perguntas', 'pontuacao_obtida', 'data_realizacao', 'concluido')
    list_filter = ('concluido', 'data_realizacao', 'quiz', 'estudante')
    search_fields = ('estudante__nome', 'quiz__titulo')
    readonly_fields = ('data_realizacao',)
    ordering = ('-data_realizacao',)
    
    fieldsets = (
        ('Informações do Resultado', {
            'fields': ('estudante', 'quiz', 'concluido')
        }),
        ('Estatísticas', {
            'fields': ('acertos', 'total_perguntas', 'pontuacao_obtida', 'tempo_gasto')
        }),
        ('Dados do Sistema', {
            'fields': ('data_realizacao',),
            'classes': ('collapse',)
        }),
    )


# Desregistra o UserAdmin padrão e registra o customizado
admin.site.unregister(User)
admin.site.register(User, CustomUserAdmin)

# Configurações gerais do admin
admin.site.site_header = "LogiCash - Administração"
admin.site.site_title = "LogiCash Admin"
admin.site.index_title = "Painel de Administração do LogiCash"
admin.site.register(Modulo)
admin.site.register(Desafio)
admin.site.register(ProgressoDesafio)