// BikeRent JavaScript Application

// Global variables
let currentUser = null;
let currentMap = null;
let bikeMarkers = [];

// Initialize the app when DOM is loaded
document.addEventListener('DOMContentLoaded', function() {
    // Initialize tooltips if Bootstrap is available
    if (typeof bootstrap !== 'undefined') {
        var tooltipTriggerList = [].slice.call(document.querySelectorAll('[data-bs-toggle="tooltip"]'));
        var tooltipList = tooltipTriggerList.map(function (tooltipTriggerEl) {
            return new bootstrap.Tooltip(tooltipTriggerEl);
        });
    }
    
    // Add smooth scrolling to anchor links
    document.querySelectorAll('a[href^="#"]').forEach(anchor => {
        anchor.addEventListener('click', function (e) {
            e.preventDefault();
            const target = document.querySelector(this.getAttribute('href'));
            if (target) {
                target.scrollIntoView({
                    behavior: 'smooth',
                    block: 'start'
                });
            }
        });
    });
    
    // Initialize page-specific functionality
    initPageSpecific();
});

// Initialize page-specific functionality based on current page
function initPageSpecific() {
    const path = window.location.pathname;
    
    if (path.includes('/map')) {
        initMapPage();
    } else if (path.includes('/payment')) {
        initPaymentPage();
    } else if (path.includes('/dashboard')) {
        initDashboardPage();
    }
}

// Map page initialization
function initMapPage() {
    // Auto-refresh bike data every 30 seconds
    setInterval(refreshBikeData, 30000);
    
    // Add loading states to filter buttons
    const filterButton = document.querySelector('[onclick="applyFilters()"]');
    if (filterButton) {
        filterButton.addEventListener('click', function() {
            showLoading(this);
        });
    }
}

// Payment page initialization
function initPaymentPage() {
    // Add form validation
    const paymentForm = document.querySelector('form[action*="checkout-session"]');
    if (paymentForm) {
        paymentForm.addEventListener('submit', function(e) {
            const submitBtn = this.querySelector('button[type="submit"]');
            showLoading(submitBtn);
            submitBtn.disabled = true;
        });
    }
}

// Dashboard page initialization
function initDashboardPage() {
    // Auto-refresh reservation data every 60 seconds
    setInterval(refreshDashboard, 60000);
}

// Show loading state on button
function showLoading(button) {
    const originalText = button.innerHTML;
    button.innerHTML = '<div class="loading"></div> Carregando...';
    button.disabled = true;
    
    setTimeout(() => {
        button.innerHTML = originalText;
        button.disabled = false;
    }, 2000);
}

// Refresh bike data (for map page)
function refreshBikeData() {
    fetch('/api/bikes')
        .then(response => response.json())
        .then(data => {
            // Update bike markers on map if map exists
            if (window.addBikeMarkers && typeof window.addBikeMarkers === 'function') {
                window.addBikeMarkers(data);
            }
        })
        .catch(error => {
            console.error('Erro ao atualizar dados das bikes:', error);
        });
}

// Refresh dashboard data
function refreshDashboard() {
    // In a real app, this would fetch updated reservation data
    console.log('Atualizando dados do dashboard...');
}

// Utility function to format currency
function formatCurrency(value) {
    return new Intl.NumberFormat('pt-BR', {
        style: 'currency',
        currency: 'BRL'
    }).format(value);
}

// Utility function to format date
function formatDate(dateString) {
    const date = new Date(dateString);
    return new Intl.DateTimeFormat('pt-BR', {
        day: '2-digit',
        month: '2-digit',
        year: 'numeric',
        hour: '2-digit',
        minute: '2-digit'
    }).format(date);
}

// Show notification
function showNotification(message, type = 'info') {
    // Create notification element
    const notification = document.createElement('div');
    notification.className = `alert alert-${type === 'error' ? 'danger' : type} alert-dismissible fade show position-fixed`;
    notification.style.cssText = `
        top: 20px;
        right: 20px;
        z-index: 9999;
        min-width: 300px;
        box-shadow: 0 4px 8px rgba(0,0,0,0.1);
    `;
    
    notification.innerHTML = `
        <i class="fas fa-${type === 'success' ? 'check-circle' : type === 'error' ? 'exclamation-circle' : 'info-circle'} me-2"></i>
        ${message}
        <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
    `;
    
    document.body.appendChild(notification);
    
    // Auto-remove after 5 seconds
    setTimeout(() => {
        if (notification.parentNode) {
            notification.remove();
        }
    }, 5000);
}

// Confirm action
function confirmAction(message, callback) {
    if (confirm(message)) {
        callback();
    }
}

// Enhanced phone number formatting
function formatPhoneNumber(input) {
    // Remove all non-numeric characters
    let value = input.value.replace(/\D/g, '');
    let formattedValue = '';
    
    if (value.length > 0) {
        formattedValue += '(' + value.substring(0, 2);
    }
    if (value.length >= 3) {
        formattedValue += ') ' + value.substring(2, 7);
    }
    if (value.length >= 8) {
        formattedValue += '-' + value.substring(7, 11);
    }
    
    input.value = formattedValue;
}

// Form validation utilities
function validateEmail(email) {
    const re = /^[^\s@]+@[^\s@]+\.[^\s@]+$/;
    return re.test(email);
}

function validatePhone(phone) {
    const re = /^\(\d{2}\) \d{4,5}-\d{4}$/;
    return re.test(phone);
}

function validateForm(formSelector) {
    const form = document.querySelector(formSelector);
    if (!form) return false;
    
    let isValid = true;
    const inputs = form.querySelectorAll('input[required]');
    
    inputs.forEach(input => {
        if (!input.value.trim()) {
            showFieldError(input, 'Este campo é obrigatório');
            isValid = false;
        } else if (input.type === 'email' && !validateEmail(input.value)) {
            showFieldError(input, 'Email inválido');
            isValid = false;
        } else if (input.name === 'phone' && !validatePhone(input.value)) {
            showFieldError(input, 'Telefone inválido');
            isValid = false;
        } else {
            clearFieldError(input);
        }
    });
    
    return isValid;
}

function showFieldError(input, message) {
    clearFieldError(input);
    
    const errorDiv = document.createElement('div');
    errorDiv.className = 'text-danger small mt-1 field-error';
    errorDiv.textContent = message;
    
    input.parentNode.appendChild(errorDiv);
    input.classList.add('is-invalid');
}

function clearFieldError(input) {
    const existingError = input.parentNode.querySelector('.field-error');
    if (existingError) {
        existingError.remove();
    }
    input.classList.remove('is-invalid');
}

// Local storage utilities for user preferences
function saveUserPreference(key, value) {
    try {
        localStorage.setItem(`bikerent_${key}`, JSON.stringify(value));
    } catch (e) {
        console.warn('Could not save user preference:', e);
    }
}

function getUserPreference(key, defaultValue = null) {
    try {
        const item = localStorage.getItem(`bikerent_${key}`);
        return item ? JSON.parse(item) : defaultValue;
    } catch (e) {
        console.warn('Could not get user preference:', e);
        return defaultValue;
    }
}

// Animation utilities
function animateIn(element, animation = 'fadeIn') {
    element.style.opacity = '0';
    element.style.transform = 'translateY(20px)';
    element.style.transition = 'all 0.3s ease';
    
    setTimeout(() => {
        element.style.opacity = '1';
        element.style.transform = 'translateY(0)';
    }, 100);
}

function animateOut(element, callback) {
    element.style.transition = 'all 0.3s ease';
    element.style.opacity = '0';
    element.style.transform = 'translateY(-20px)';
    
    setTimeout(() => {
        if (callback) callback();
    }, 300);
}

// Export functions for global use
window.BikeRent = {
    showNotification,
    confirmAction,
    formatCurrency,
    formatDate,
    formatPhoneNumber,
    validateForm,
    showLoading,
    saveUserPreference,
    getUserPreference,
    animateIn,
    animateOut
};