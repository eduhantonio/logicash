/**
 * LogiCash - JavaScript para Autenticação
 * Funcionalidades específicas para telas de login, cadastro e redefinição de senha
 */

document.addEventListener('DOMContentLoaded', function() {
    
    // Inicialização das funcionalidades
    initAuthAnimations();
    initFormValidation();
    initPasswordStrength();
    initAutoHideMessages();
    initFormFocus();
    
    console.log('🔐 LogiCash Auth carregado com sucesso!');
});

/**
 * Inicializa animações específicas para autenticação
 */
function initAuthAnimations() {
    // Animação de entrada do container principal
    const authContainer = document.querySelector('.auth-container');
    if (authContainer) {
        authContainer.style.opacity = '0';
        authContainer.style.transform = 'translateY(30px)';
        
        setTimeout(() => {
            authContainer.style.transition = 'all 0.8s ease-out';
            authContainer.style.opacity = '1';
            authContainer.style.transform = 'translateY(0)';
        }, 100);
    }
    
    // Animação sequencial dos campos do formulário
    const formGroups = document.querySelectorAll('.form-group');
    formGroups.forEach((group, index) => {
        group.style.opacity = '0';
        group.style.transform = 'translateY(20px)';
        
        setTimeout(() => {
            group.style.transition = 'all 0.6s ease-out';
            group.style.opacity = '1';
            group.style.transform = 'translateY(0)';
        }, 200 + (index * 100));
    });
    
    // Efeito pulsante no logo
    const logoIcon = document.querySelector('.auth-logo i');
    if (logoIcon) {
        setInterval(() => {
            logoIcon.style.transform = 'scale(1.1)';
            setTimeout(() => {
                logoIcon.style.transform = 'scale(1)';
            }, 500);
        }, 3000);
    }
}

/**
 * Inicializa validação de formulários
 */
function initFormValidation() {
    const forms = document.querySelectorAll('.auth-form');
    
    forms.forEach(form => {
        form.addEventListener('submit', function(e) {
            const submitBtn = form.querySelector('.auth-btn');
            if (submitBtn && !submitBtn.disabled) {
                showLoadingState(submitBtn);
            }
        });
        
        // Validação em tempo real para campos obrigatórios
        const requiredInputs = form.querySelectorAll('input[required]');
        requiredInputs.forEach(input => {
            input.addEventListener('blur', validateRequiredField);
            input.addEventListener('input', clearFieldError);
        });
    });
}

/**
 * Valida campo obrigatório
 */
function validateRequiredField(e) {
    const input = e.target;
    const value = input.value.trim();
    
    if (!value) {
        showFieldError(input, 'Este campo é obrigatório');
        return false;
    } else {
        clearFieldError(e);
        return true;
    }
}

/**
 * Mostra erro em campo específico
 */
function showFieldError(input, message) {
    clearFieldError({ target: input });
    
    input.style.borderColor = '#dc3545';
    input.style.backgroundColor = '#f8d7da';
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'field-error';
    errorDiv.innerHTML = `<small class="text-danger">${message}</small>`;
    
    input.parentNode.appendChild(errorDiv);
}

/**
 * Remove erro de campo específico
 */
function clearFieldError(e) {
    const input = e.target;
    const errorDiv = input.parentNode.querySelector('.field-error');
    
    if (errorDiv) {
        errorDiv.remove();
    }
    
    input.style.borderColor = '';
    input.style.backgroundColor = '';
}

/**
 * Inicializa indicador de força da senha
 */
function initPasswordStrength() {
    const passwordInputs = document.querySelectorAll('input[type="password"]');
    
    passwordInputs.forEach(input => {
        if (input.id.includes('password1') || input.id.includes('new_password1')) {
            input.addEventListener('input', function() {
                const strength = calculatePasswordStrength(this.value);
                updatePasswordStrengthIndicator(this, strength);
            });
        }
        
        // Validação de confirmação de senha
        if (input.id.includes('password2') || input.id.includes('new_password2')) {
            const password1Id = input.id.replace('2', '1');
            const password1Input = document.getElementById(password1Id);
            
            if (password1Input) {
                input.addEventListener('input', function() {
                    validatePasswordMatch(password1Input.value, this.value, this);
                });
            }
        }
    });
}

/**
 * Calcula força da senha
 */
function calculatePasswordStrength(password) {
    let strength = 0;
    const checks = {
        length: password.length >= 8,
        lowercase: /[a-z]/.test(password),
        uppercase: /[A-Z]/.test(password),
        number: /[0-9]/.test(password),
        special: /[^A-Za-z0-9]/.test(password)
    };
    
    strength = Object.values(checks).filter(Boolean).length;
    
    return { strength, checks };
}

/**
 * Atualiza indicador visual de força da senha
 */
function updatePasswordStrengthIndicator(input, strengthData) {
    let indicator = document.getElementById('password-strength');
    if (!indicator) {
        indicator = document.createElement('div');
        indicator.id = 'password-strength';
        indicator.className = 'password-strength-indicator';
        input.parentNode.appendChild(indicator);
    }
    
    const { strength, checks } = strengthData;
    const levels = ['Muito Fraca', 'Fraca', 'Regular', 'Boa', 'Muito Forte'];
    const colors = ['#dc3545', '#fd7e14', '#ffc107', '#20c997', '#198754'];
    
    const percentage = (strength / 5) * 100;
    const color = colors[strength - 1] || '#6c757d';
    const level = levels[strength - 1] || 'Muito Fraca';
    
    indicator.innerHTML = `
        <div class="strength-bar">
            <div class="strength-fill" style="width: ${percentage}%; background-color: ${color}; transition: all 0.3s ease;"></div>
        </div>
        <small class="strength-text" style="color: ${color}; font-weight: 600;">${level}</small>
    `;
    
    // Atualizar cor da borda do input
    if (strength >= 3) {
        input.style.borderColor = color;
    } else {
        input.style.borderColor = '#dc3545';
    }
}

/**
 * Valida se as senhas coincidem
 */
function validatePasswordMatch(password1, password2, password2Input) {
    if (password2.length === 0) {
        clearFieldError({ target: password2Input });
        return;
    }
    
    if (password1 === password2) {
        password2Input.style.borderColor = '#198754';
        password2Input.style.backgroundColor = '#d1e7dd';
        clearFieldError({ target: password2Input });
    } else {
        password2Input.style.borderColor = '#dc3545';
        password2Input.style.backgroundColor = '#f8d7da';
        showFieldError(password2Input, 'As senhas não coincidem');
    }
}

/**
 * Inicializa auto-hide de mensagens
 */
function initAutoHideMessages() {
    const alerts = document.querySelectorAll('.alert');
    
    alerts.forEach(alert => {
        // Adicionar botão de fechar se não existir
        if (!alert.querySelector('.btn-close')) {
            const closeBtn = document.createElement('button');
            closeBtn.type = 'button';
            closeBtn.className = 'btn-close';
            closeBtn.innerHTML = '&times;';
            closeBtn.addEventListener('click', () => alert.remove());
            alert.appendChild(closeBtn);
        }
        
        // Auto-hide após 5 segundos
        setTimeout(() => {
            if (alert.parentNode) {
                alert.style.opacity = '0';
                alert.style.transform = 'translateX(100%)';
                
                setTimeout(() => {
                    if (alert.parentNode) {
                        alert.parentNode.removeChild(alert);
                    }
                }, 300);
            }
        }, 5000);
    });
}

/**
 * Inicializa efeitos de foco nos inputs
 */
function initFormFocus() {
    const inputs = document.querySelectorAll('.auth-input');
    
    inputs.forEach(input => {
        // Efeito de foco
        input.addEventListener('focus', function() {
            this.parentElement.classList.add('focused');
            this.style.transform = 'translateY(-1px)';
        });
        
        input.addEventListener('blur', function() {
            if (!this.value.trim()) {
                this.parentElement.classList.remove('focused');
            }
            this.style.transform = 'translateY(0)';
        });
        
        // Verificar se já tem valor ao carregar
        if (input.value.trim()) {
            input.parentElement.classList.add('focused');
        }
        
        // Efeito de hover
        input.addEventListener('mouseenter', function() {
            if (document.activeElement !== this) {
                this.style.borderColor = 'var(--secondary-green)';
            }
        });
        
        input.addEventListener('mouseleave', function() {
            if (document.activeElement !== this) {
                this.style.borderColor = '';
            }
        });
    });
}

/**
 * Mostra estado de loading no botão
 */
function showLoadingState(button) {
    button.classList.add('loading');
    button.disabled = true;
    
    // Simular loading por alguns segundos (em produção, isso seria controlado pela resposta do servidor)
    setTimeout(() => {
        button.classList.remove('loading');
        button.disabled = false;
    }, 3000);
}

/**
 * Validação de email
 */
function validateEmail(email) {
    const emailRegex = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return emailRegex.test(email);
}

/**
 * Formatação de campos específicos
 */
function initFieldFormatting() {
    // Formatação de data
    const dateInputs = document.querySelectorAll('input[type="date"]');
    dateInputs.forEach(input => {
        input.addEventListener('change', function() {
            // Validação de idade mínima (13 anos)
            if (this.value) {
                const birthDate = new Date(this.value);
                const today = new Date();
                const age = today.getFullYear() - birthDate.getFullYear();
                
                if (age < 13) {
                    showFieldError(this, 'Você deve ter pelo menos 13 anos');
                } else {
                    clearFieldError({ target: this });
                }
            }
        });
    });
    
    // Formatação de username
    const usernameInputs = document.querySelectorAll('input[name="username"]');
    usernameInputs.forEach(input => {
        input.addEventListener('input', function() {
            // Remover caracteres especiais
            this.value = this.value.replace(/[^a-zA-Z0-9_]/g, '');
            
            // Validação de comprimento mínimo
            if (this.value.length > 0 && this.value.length < 3) {
                showFieldError(this, 'Nome de usuário deve ter pelo menos 3 caracteres');
            } else {
                clearFieldError({ target: this });
            }
        });
    });
}

/**
 * Efeitos visuais para botões
 */
function initButtonEffects() {
    const buttons = document.querySelectorAll('.auth-btn, .btn');
    
    buttons.forEach(button => {
        button.addEventListener('mouseenter', function() {
            if (!this.disabled) {
                this.style.transform = 'translateY(-2px)';
            }
        });
        
        button.addEventListener('mouseleave', function() {
            if (!this.disabled) {
                this.style.transform = 'translateY(0)';
            }
        });
        
        button.addEventListener('mousedown', function() {
            if (!this.disabled) {
                this.style.transform = 'translateY(1px)';
            }
        });
        
        button.addEventListener('mouseup', function() {
            if (!this.disabled) {
                this.style.transform = 'translateY(-2px)';
            }
        });
    });
}

/**
 * Inicializa todas as funcionalidades quando o DOM estiver pronto
 */
document.addEventListener('DOMContentLoaded', function() {
    initFieldFormatting();
    initButtonEffects();
});

/**
 * Função para debug - mostra informações de autenticação
 */
function showAuthInfo() {
    console.group('🔐 LogiCash Auth Info');
    console.log('📝 Formulários carregados');
    console.log('🔒 Validações ativas');
    console.log('🎨 Animações funcionando');
    console.log('💪 Indicador de força da senha');
    console.groupEnd();
}

// Exposição de funções para uso global (opcional)
window.LogiCashAuth = {
    validateEmail,
    calculatePasswordStrength,
    showAuthInfo,
    showLoadingState
};
