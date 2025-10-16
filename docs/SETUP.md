# 🚀 LogiCash - Guia de Configuração

## 📋 Pré-requisitos
- Python 3.8 ou superior
- pip (gerenciador de pacotes Python)
- Git (para clonar o repositório)

## 🛠️ Configuração do Projeto

### 1. Ativar o Ambiente Virtual
```bash
# Windows
.\env\Scripts\activate

# macOS/Linux
source env/bin/activate
```

### 2. Instalar Dependências
```bash
pip install -r requirements.txt
```

### 3. Executar Migrações
```bash
# Criar migrações
python manage.py makemigrations

# Aplicar migrações
python manage.py migrate
```

### 4. Criar Superusuário (Administrador)
```bash
python manage.py createsuperuser
```

### 5. Coletar Arquivos Estáticos
```bash
python manage.py collectstatic
```

### 6. Executar o Servidor
```bash
python manage.py runserver
```

## 🎮 Acessando o LogiCash

### URLs Disponíveis:
- **Dashboard**: http://127.0.0.1:8000/dashboard/
- **Admin**: http://127.0.0.1:8000/admin/
- **Página Inicial**: http://127.0.0.1:8000/

### Credenciais de Teste:
- Faça login com o superusuário criado no passo 4
- Ou crie um usuário normal através do admin

## 🧪 Executando Testes
```bash
python manage.py test
```

## 📁 Estrutura de Arquivos Criados

```
logicash/
├── game/
│   ├── models.py          # Modelos do LogiCash
│   ├── views.py           # Views do dashboard
│   ├── urls.py            # URLs do app
│   ├── admin.py           # Configuração do admin
│   └── tests.py           # Testes unitários
├── templates/
│   └── index.html         # Template do dashboard
├── static/
│   ├── css/
│   │   └── style.css      # Estilos do LogiCash
│   └── js/
│       └── main.js        # JavaScript interativo
└── SETUP.md              # Este arquivo
```

## 🎨 Funcionalidades Implementadas

### ✅ Dashboard Completo
- **Menu lateral responsivo** com navegação
- **Cards de estatísticas** (pontuação, nível, quizzes, taxa de acertos)
- **Seção de conquistas** com badges desbloqueadas
- **Próximas metas** para motivar o progresso
- **Histórico de progresso** recente
- **Design gamificado** com animações e transições

### ✅ Sistema de Gamificação
- **Sistema de pontuação** com cálculo automático de níveis
- **Conquistas desbloqueáveis** com critérios configuráveis
- **Progresso visual** com barras animadas
- **Estatísticas detalhadas** de performance

### ✅ Interface Responsiva
- **Mobile-first** design
- **Menu hambúrguer** para dispositivos móveis
- **Animações suaves** e efeitos visuais
- **Tema LogiCash** com cores personalizadas

### ✅ Backend Robusto
- **Modelos completos** para todo o sistema
- **Admin interface** customizada
- **Testes unitários** abrangentes
- **Tratamento de erros** adequado

## 🎯 Próximos Passos

1. **Criar quizzes** através do admin
2. **Configurar conquistas** com critérios específicos
3. **Adicionar mais funcionalidades** como ranking
4. **Implementar sistema de login** completo
5. **Adicionar mais temas** e personalizações

## 🐛 Solução de Problemas

### Erro de Migração
```bash
# Se houver conflitos de migração
python manage.py migrate --fake-initial
```

### Problemas com Arquivos Estáticos
```bash
# Limpar cache e recolher arquivos
python manage.py collectstatic --clear
```

### Erro de Permissão (Windows)
```bash
# Executar como administrador se necessário
```

## 📞 Suporte

Para dúvidas ou problemas:
1. Verifique os logs do Django no terminal
2. Consulte a documentação do Django
3. Execute os testes para verificar a integridade

---

**🎉 Parabéns! O LogiCash Dashboard está pronto para uso!**
