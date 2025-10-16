from django.db import models
from django.contrib.auth.models import User
from django.core.validators import MinValueValidator, MaxValueValidator


class Estudante(models.Model):
    """
    Modelo que estende o usuário padrão do Django com informações específicas do LogiCash
    """
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='estudante')
    nome = models.CharField(max_length=100, help_text="Nome completo do estudante")
    data_nascimento = models.DateField(null=True, blank=True)
    escola = models.CharField(max_length=200, null=True, blank=True)
    serie = models.CharField(max_length=50, null=True, blank=True)
    data_cadastro = models.DateTimeField(auto_now_add=True)
    avatar = models.ImageField(upload_to='avatars/', null=True, blank=True)
    
    class Meta:
        verbose_name = "Estudante"
        verbose_name_plural = "Estudantes"
        ordering = ['nome']
    
    def __str__(self):
        return self.nome or self.user.username


class Quiz(models.Model):
    """
    Modelo para representar um quiz de educação financeira
    """
    titulo = models.CharField(max_length=200)
    descricao = models.TextField()
    nivel_dificuldade = models.IntegerField(
        validators=[MinValueValidator(1), MaxValueValidator(5)],
        help_text="Nível de dificuldade de 1 a 5"
    )
    tema = models.CharField(max_length=100, help_text="Ex: Poupança, Investimentos, Cartão de Crédito")
    tempo_limite = models.IntegerField(null=True, blank=True, help_text="Tempo limite em minutos")
    pontos_base = models.IntegerField(default=10, help_text="Pontos base para completar o quiz")
    ativo = models.BooleanField(default=True)
    data_criacao = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Quiz"
        verbose_name_plural = "Quizzes"
        ordering = ['nivel_dificuldade', 'titulo']
    
    def __str__(self):
        return f"{self.titulo} (Nível {self.nivel_dificuldade})"


class Pergunta(models.Model):
    """
    Modelo para representar uma pergunta dentro de um quiz
    """
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='perguntas')
    texto = models.TextField()
    explicacao = models.TextField(null=True, blank=True, help_text="Explicação da resposta correta")
    ordem = models.IntegerField(default=1)
    pontos = models.IntegerField(default=1)
    
    class Meta:
        verbose_name = "Pergunta"
        verbose_name_plural = "Perguntas"
        ordering = ['quiz', 'ordem']
        unique_together = ['quiz', 'ordem']
    
    def __str__(self):
        return f"{self.quiz.titulo} - Pergunta {self.ordem}"


class Resposta(models.Model):
    """
    Modelo para representar as opções de resposta de uma pergunta
    """
    pergunta = models.ForeignKey(Pergunta, on_delete=models.CASCADE, related_name='respostas')
    texto = models.CharField(max_length=500)
    correta = models.BooleanField(default=False)
    ordem = models.IntegerField(default=1)
    
    class Meta:
        verbose_name = "Resposta"
        verbose_name_plural = "Respostas"
        ordering = ['pergunta', 'ordem']
    
    def __str__(self):
        return f"{self.pergunta} - {self.texto[:50]}"


class Resultado(models.Model):
    """
    Modelo para armazenar os resultados de um quiz realizado por um estudante
    """
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='resultados')
    quiz = models.ForeignKey(Quiz, on_delete=models.CASCADE, related_name='resultados')
    pontuacao_obtida = models.IntegerField(default=0)
    total_perguntas = models.IntegerField()
    acertos = models.IntegerField(default=0)
    data_realizacao = models.DateTimeField(auto_now_add=True)
    tempo_gasto = models.IntegerField(null=True, blank=True, help_text="Tempo gasto em segundos")
    concluido = models.BooleanField(default=False)
    
    class Meta:
        verbose_name = "Resultado"
        verbose_name_plural = "Resultados"
        ordering = ['-data_realizacao']
        unique_together = ['estudante', 'quiz', 'data_realizacao']
    
    def __str__(self):
        return f"{self.estudante.nome} - {self.quiz.titulo} ({self.acertos}/{self.total_perguntas})"


class Pontuacao(models.Model):
    """
    Modelo para armazenar a pontuação total acumulada de um estudante
    """
    estudante = models.OneToOneField(Estudante, on_delete=models.CASCADE, related_name='pontuacao')
    pontos_totais = models.IntegerField(default=0)
    nivel_atual = models.IntegerField(default=1)
    data_atualizacao = models.DateTimeField(auto_now=True)
    
    class Meta:
        verbose_name = "Pontuação"
        verbose_name_plural = "Pontuações"
        ordering = ['-pontos_totais']
    
    def __str__(self):
        return f"{self.estudante.nome} - {self.pontos_totais} pontos (Nível {self.nivel_atual})"
    
    def calcular_nivel(self):
        """
        Calcula o nível baseado na pontuação total
        Cada nível requer 100 pontos a mais que o anterior
        """
        return min((self.pontos_totais // 100) + 1, 100)  # Máximo nível 100
    
    def save(self, *args, **kwargs):
        self.nivel_atual = self.calcular_nivel()
        super().save(*args, **kwargs)


class Conquista(models.Model):
    """
    Modelo para representar conquistas/badges que os estudantes podem desbloquear
    """
    nome = models.CharField(max_length=100)
    descricao = models.TextField()
    icone = models.CharField(max_length=100, help_text="Nome do ícone (ex: 'trophy', 'star')")
    icone_url = models.URLField(null=True, blank=True, help_text="URL do ícone personalizado")
    criterio_pontos = models.IntegerField(null=True, blank=True, help_text="Pontos mínimos necessários")
    criterio_quizzes = models.IntegerField(null=True, blank=True, help_text="Número mínimo de quizzes completados")
    criterio_acertos = models.FloatField(null=True, blank=True, help_text="Percentual mínimo de acertos")
    nivel_dificuldade = models.IntegerField(null=True, blank=True, help_text="Nível de dificuldade específico")
    ativa = models.BooleanField(default=True)
    cor = models.CharField(max_length=7, default="#008445", help_text="Cor em hex (#008445)")
    
    class Meta:
        verbose_name = "Conquista"
        verbose_name_plural = "Conquistas"
        ordering = ['criterio_pontos', 'nome']
    
    def __str__(self):
        return self.nome


class EstudanteConquista(models.Model):
    """
    Modelo para relacionar estudantes com suas conquistas desbloqueadas
    """
    estudante = models.ForeignKey(Estudante, on_delete=models.CASCADE, related_name='conquistas')
    conquista = models.ForeignKey(Conquista, on_delete=models.CASCADE, related_name='estudantes')
    data_desbloqueio = models.DateTimeField(auto_now_add=True)
    
    class Meta:
        verbose_name = "Conquista do Estudante"
        verbose_name_plural = "Conquistas dos Estudantes"
        unique_together = ['estudante', 'conquista']
        ordering = ['-data_desbloqueio']
    
    def __str__(self):
        return f"{self.estudante.nome} - {self.conquista.nome}"
