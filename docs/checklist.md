# 📋 Checklist do Projeto LogiCash

Este é o checklist principal que cobre todas as tarefas do projeto do **LogiCash** do início ao fim.  
O projeto utiliza a metodologia **"Dividir e Conquistar"** para dividir as principais tarefas de desenvolvimento do software.

---

## Fase 1: Configuração e Planejamento Inicial 

- [X] **0.1 Configuração do Ambiente:** Instalar Python, Django, PostgreSQL/SQLite e criar repositório no GitHub.  
- [X] **0.2 Definição Arquitetural:** Especificar modelo MTV no Django, módulos principais e integração com banco de dados.  
- [X] **0.3 Protótipo de Interface:** Criar mockups iniciais das telas no Canva/Figma.  
- [X] **0.4 Modelo de Dados:** Definir MER e tabelas iniciais no DBeaver.  

---

## Fase 2: Fundamentos Independentes

### Backend ⚙️ | Lógica Central e Banco de Dados
- [ ] **1.A.1 Modelos Django:** Criar modelos `Estudante`, `Quiz`, `Pergunta`, `Resposta`, `Pontuacao`, `Conquista`.  
- [ ] **1.A.2 Regras de Negócio:** Implementar lógica de pontuação, desbloqueio de conquistas e ranking.  
- [ ] **1.A.3 Autenticação:** Configurar cadastro/login/logout de estudantes.  
- [ ] **1.A.4 Testes Unitários:** Criar testes para autenticação e persistência de dados.  

### Frontend 🎨 | Desenvolver Telas e Artes Iniciais
- [ ] **1.B.1 Configuração de Templates Django:** Criar estrutura de páginas HTML/CSS.  
- [ ] **1.B.2 Layout Inicial:** Desenvolver telas de login, cadastro e dashboard.  
- [ ] **1.B.3 Protótipo de Quiz:** Criar tela de quiz com perguntas dinâmicas.  
- [ ] **1.B.4 Testes de Navegação:** Verificar responsividade e usabilidade.  

### Gamificação 👑 | Principais Sistemas 
- [ ] **1.C.1 Sistema de Pontuação:** Implementar acúmulo de pontos por desafio.  
- [ ] **1.C.2 Sistema de Conquistas:** Implementar desbloqueio automático de medalhas.  
- [ ] **1.C.3 Ranking:** Criar ranking global dos estudantes.  
- [ ] **1.C.4 Relatórios:** Implementar histórico de desempenho por usuário.  

---

## Fase 3: Integração e Funcionalidades Essenciais

### Backend ⚙️ | Integração com o Frontend
- [ ] **2.A.1 Integração Banco de Dados–Frontend:** Conectar formulários às views Django.  
- [ ] **2.A.2 API REST (se necessário):** Criar endpoints para quizzes e pontuação.  
- [ ] **2.A.3 Sessões e Cookies:** Garantir persistência de login.  

### Frontend 🎨 | Integração com o Backend
- [ ] **2.B.1 Refinamento Visual:** Criar interface gamificada e intuitiva.  
- [ ] **2.B.2 Feedback Imediato:** Exibir respostas corretas/incorretas ao aluno.  
- [ ] **2.B.3 Painel de Estatísticas:** Mostrar progresso individual (pontuação, conquistas).  

### Gamificação 👑 | Validações de Conquistas
- [ ] **2.C.1 Lógica de Conquistas:** Configurar critérios de desbloqueio (ex.: 10 quizzes concluídos).  
- [ ] **2.C.2 Relatórios Detalhados:** Criar histórico com gráficos e tabelas.  
- [ ] **2.C.3 Testes de Ranking:** Validar consistência da classificação.  

---

## Fase 4: Funcionalidades Avançadas e Refinamentos

### Backend ⚙️
- [ ] **3.A.1 Painel de Administração:** Criar área para cadastrar e editar quizzes.  
- [ ] **3.A.2 Exportação de Relatórios:** Implementar exportação para CSV/Excel.  
- [ ] **3.A.3 API Pública (opcional):** Permitir integração externa.  

### Frontend 🎨
- [ ] **3.B.1 Ajustes de Interface:** Melhorar cores, fontes e responsividade.  
- [ ] **3.B.2 Gamificação Visual:** Ícones, medalhas e badges estilizadas.  
- [ ] **3.B.3 Acessibilidade:** Implementar boas práticas (contraste, ARIA).  

### Gamificação 👑
- [ ] **3.C.1 Estatísticas Avançadas:** Gerar relatórios comparativos entre estudantes.  
- [ ] **3.C.2 Ranking Dinâmico:** Atualização em tempo real.  
- [ ] **3.C.3 Testes de Usabilidade:** Realizar testes com usuários reais.  

---

## Fase 5: Finalização e Distribuição

- [ ] **4.1 Testes de Integração:** Verificar fluxo completo do sistema.  
- [ ] **4.2 Testes de Usabilidade:** Coletar feedback de estudantes/professores.  
- [ ] **4.3 Tratamento de Erros:** Melhorar robustez e mensagens de erro.  
- [ ] **4.4 Documentação:** Criar documentação do código e manual do usuário.  
- [ ] **4.5 Deploy:** Configurar ambiente de produção (Heroku, Railway ou servidor Django).  
- [ ] **4.6 Apresentação Final:** Preparar slides e demonstração funcional para banca.  

---
