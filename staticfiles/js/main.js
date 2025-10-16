/**
 * LogiCash - JavaScript para Dashboard
 * Interações e animações do dashboard gamificado
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Inicialização das funcionalidades
    initMobileMenu();
    initAnimations();
    initProgressBars();
    initAchievementCards();
    initTooltips();
    initAutoHideMessages();
    
    console.log('🎮 LogiCash Dashboard carregado com sucesso!');
});

/**
 * Inicializa o menu mobile (hambúrguer)
 */
function initMobileMenu() {
    const mobileMenuBtn = document.querySelector('.mobile-menu-btn');
    const sidebar = document.querySelector('.sidebar');
    
    if (mobileMenuBtn && sidebar) {
        mobileMenuBtn.addEventListener('click', function() {
            sidebar.classList.toggle('open');
            this.classList.toggle('active');
            
            // Animação do ícone hambúrguer
            const icon = this.querySelector('i');
            if (sidebar.classList.contains('open')) {
                icon.classList.remove('fa-bars');
                icon.classList.add('fa-times');
            } else {
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
        
        // Fechar menu ao clicar fora
        document.addEventListener('click', function(e) {
            if (window.innerWidth <= 768 && 
                !sidebar.contains(e.target) && 
                !mobileMenuBtn.contains(e.target) && 
                sidebar.classList.contains('open')) {
                sidebar.classList.remove('open');
                mobileMenuBtn.classList.remove('active');
                const icon = mobileMenuBtn.querySelector('i');
                icon.classList.remove('fa-times');
                icon.classList.add('fa-bars');
            }
        });
    }
}

/**
 * Inicializa animações de entrada dos elementos
 */
function initAnimations() {
    // Anima os cards de estatísticas
    const statCards = document.querySelectorAll('.stat-card');
    statCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.6s ease-out';
            card.style.opacity = '1';
            card.style.transform = 'translateY(0)';
        }, index * 150);
    });
    
    // Anima os cards de conquistas
    const achievementCards = document.querySelectorAll('.achievement-card');
    achievementCards.forEach((card, index) => {
        card.style.opacity = '0';
        card.style.transform = 'scale(0.8)';
        
        setTimeout(() => {
            card.style.transition = 'all 0.5s ease-out';
            card.style.opacity = '1';
            card.style.transform = 'scale(1)';
        }, (statCards.length * 150) + (index * 100));
    });
}

/**
 * Inicializa as barras de progresso com animação
 */
function initProgressBars() {
    const progressBars = document.querySelectorAll('.progress-fill');
    
    progressBars.forEach(bar => {
        const width = bar.getAttribute('data-width') || bar.style.width || '0%';
        bar.style.width = '0%';
        
        setTimeout(() => {
            bar.style.transition = 'width 1.5s ease-out';
            bar.style.width = width;
        }, 500);
    });
}

/**
 * Adiciona interações aos cards de conquistas
 */
function initAchievementCards() {
    const achievementCards = document.querySelectorAll('.achievement-card');
    
    achievementCards.forEach(card => {
        // Efeito de hover com bounce
        card.addEventListener('mouseenter', function() {
            this.style.transform = 'translateY(-5px) scale(1.02)';
        });
        
        card.addEventListener('mouseleave', function() {
            this.style.transform = 'translateY(0) scale(1)';
        });
        
        // Efeito de clique
        card.addEventListener('click', function() {
            this.style.transform = 'translateY(-3px) scale(0.98)';
            setTimeout(() => {
                this.style.transform = 'translateY(-5px) scale(1.02)';
            }, 150);
        });
    });
}

/**
 * Inicializa tooltips para elementos informativos
 */
function initTooltips() {
    const tooltipElements = document.querySelectorAll('[data-tooltip]');
    
    tooltipElements.forEach(element => {
        element.addEventListener('mouseenter', showTooltip);
        element.addEventListener('mouseleave', hideTooltip);
        element.addEventListener('mousemove', updateTooltipPosition);
    });
}

/**
 * Mostra tooltip
 */
function showTooltip(e) {
    const tooltipText = e.target.getAttribute('data-tooltip');
    if (!tooltipText) return;
    
    const tooltip = document.createElement('div');
    tooltip.className = 'tooltip';
    tooltip.textContent = tooltipText;
    tooltip.style.cssText = `
        position: absolute;
        background: var(--dark-gray);
        color: var(--white);
        padding: 0.5rem 1rem;
        border-radius: 6px;
        font-size: 0.8rem;
        z-index: 1000;
        pointer-events: none;
        opacity: 0;
        transition: opacity 0.3s ease;
        max-width: 200px;
        word-wrap: break-word;
    `;
    
    document.body.appendChild(tooltip);
    
    setTimeout(() => {
        tooltip.style.opacity = '1';
    }, 10);
    
    e.target._tooltip = tooltip;
    updateTooltipPosition(e);
}

/**
 * Esconde tooltip
 */
function hideTooltip(e) {
    const tooltip = e.target._tooltip;
    if (tooltip) {
        tooltip.style.opacity = '0';
        setTimeout(() => {
            if (tooltip.parentNode) {
                tooltip.parentNode.removeChild(tooltip);
            }
        }, 300);
        delete e.target._tooltip;
    }
}

/**
 * Atualiza posição do tooltip
 */
function updateTooltipPosition(e) {
    const tooltip = e.target._tooltip;
    if (!tooltip) return;
    
    const rect = e.target.getBoundingClientRect();
    tooltip.style.left = rect.left + (rect.width / 2) - (tooltip.offsetWidth / 2) + 'px';
    tooltip.style.top = rect.top - tooltip.offsetHeight - 10 + 'px';
}

/**
 * Auto-hide das mensagens do Django após 5 segundos
 */
function initAutoHideMessages() {
    const messages = document.querySelectorAll('.alert');
    
    messages.forEach(message => {
        setTimeout(() => {
            message.style.opacity = '0';
            message.style.transform = 'translateX(100%)';
            
            setTimeout(() => {
                if (message.parentNode) {
                    message.parentNode.removeChild(message);
                }
            }, 300);
        }, 5000);
    });
}

/**
 * Função para animar números (contador)
 */
function animateNumber(element, start, end, duration = 2000) {
    const startTime = performance.now();
    const difference = end - start;
    
    function updateNumber(currentTime) {
        const elapsed = currentTime - startTime;
        const progress = Math.min(elapsed / duration, 1);
        
        // Easing function (ease-out)
        const easeOut = 1 - Math.pow(1 - progress, 3);
        const current = Math.floor(start + (difference * easeOut));
        
        element.textContent = current.toLocaleString('pt-BR');
        
        if (progress < 1) {
            requestAnimationFrame(updateNumber);
        } else {
            element.textContent = end.toLocaleString('pt-BR');
        }
    }
    
    requestAnimationFrame(updateNumber);
}

/**
 * Inicializa animação dos números nos cards de estatísticas
 */
function initNumberAnimations() {
    const statValues = document.querySelectorAll('.stat-card-value');
    
    statValues.forEach(element => {
        const finalValue = parseInt(element.textContent.replace(/[^\d]/g, ''));
        if (!isNaN(finalValue) && finalValue > 0) {
            element.textContent = '0';
            setTimeout(() => {
                animateNumber(element, 0, finalValue);
            }, 1000);
        }
    });
}

/**
 * Função para criar confetti quando conquista é desbloqueada
 */
function createConfetti() {
    const colors = ['#008445', '#2aea8e', '#fcfffe', '#323232'];
    const confettiCount = 50;
    
    for (let i = 0; i < confettiCount; i++) {
        const confetti = document.createElement('div');
        confetti.style.cssText = `
            position: fixed;
            width: 10px;
            height: 10px;
            background: ${colors[Math.floor(Math.random() * colors.length)]};
            top: -10px;
            left: ${Math.random() * 100}%;
            z-index: 9999;
            pointer-events: none;
        `;
        
        document.body.appendChild(confetti);
        
        // Animação de queda
        const animation = confetti.animate([
            { transform: 'translateY(0px) rotate(0deg)', opacity: 1 },
            { transform: `translateY(${window.innerHeight + 100}px) rotate(360deg)`, opacity: 0 }
        ], {
            duration: Math.random() * 3000 + 2000,
            easing: 'cubic-bezier(0.25, 0.46, 0.45, 0.94)'
        });
        
        animation.onfinish = () => {
            if (confetti.parentNode) {
                confetti.parentNode.removeChild(confetti);
            }
        };
    }
}

/**
 * Função para simular desbloqueio de conquista (para demonstração)
 */
function simulateAchievementUnlock() {
    const achievementCards = document.querySelectorAll('.achievement-card');
    if (achievementCards.length > 0) {
        const randomCard = achievementCards[Math.floor(Math.random() * achievementCards.length)];
        
        // Efeito visual
        randomCard.style.animation = 'pulse 0.6s ease-in-out';
        randomCard.style.boxShadow = '0 0 30px rgba(46, 234, 142, 0.6)';
        
        // Confetti
        createConfetti();
        
        // Reset após animação
        setTimeout(() => {
            randomCard.style.animation = '';
            randomCard.style.boxShadow = '';
        }, 600);
    }
}

/**
 * Função para atualizar progresso em tempo real
 */
function updateProgress(progressElement, newValue, maxValue) {
    const percentage = (newValue / maxValue) * 100;
    progressElement.style.width = `${Math.min(percentage, 100)}%`;
    
    // Adiciona efeito visual
    progressElement.style.background = `linear-gradient(90deg, 
        var(--primary-green) 0%, 
        var(--secondary-green) ${percentage}%, 
        var(--light-gray) ${percentage}%, 
        var(--light-gray) 100%)`;
}

/**
 * Função para verificar se há novas conquistas (simulação)
 */
function checkForNewAchievements() {
    // Esta função seria chamada periodicamente para verificar conquistas
    // Por enquanto, é apenas uma simulação
    const shouldUnlock = Math.random() < 0.1; // 10% de chance
    
    if (shouldUnlock) {
        simulateAchievementUnlock();
    }
}

/**
 * Inicializa todas as animações de números após o carregamento
 */
setTimeout(() => {
    initNumberAnimations();
}, 1500);

/**
 * Verifica novas conquistas a cada 30 segundos (para demonstração)
 */
setInterval(checkForNewAchievements, 30000);

/**
 * Função para debug - mostra informações do dashboard
 */
function showDashboardInfo() {
    console.group('🎮 LogiCash Dashboard Info');
    console.log('📊 Estatísticas carregadas');
    console.log('🏆 Conquistas desbloqueadas');
    console.log('📈 Progresso atualizado');
    console.log('🎨 Animações ativas');
    console.groupEnd();
}

// Exposição de funções para uso global (opcional)
window.LogiCash = {
    createConfetti,
    simulateAchievementUnlock,
    updateProgress,
    showDashboardInfo
};
