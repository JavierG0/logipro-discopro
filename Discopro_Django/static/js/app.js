// Discopro JavaScript - App.js

// ===== CONFIGURACIÓN GLOBAL =====
const API_BASE_URL = '/api/';
const CSRF_TOKEN = document.querySelector('[name=csrfmiddlewaretoken]')?.value || '';

// ===== UTILIDADES =====
function getCookie(name) {
    let cookieValue = null;
    if (document.cookie && document.cookie !== '') {
        const cookies = document.cookie.split(';');
        for (let i = 0; i < cookies.length; i++) {
            const cookie = cookies[i].trim();
            if (cookie.substring(0, name.length + 1) === (name + '=')) {
                cookieValue = decodeURIComponent(cookie.substring(name.length + 1));
                break;
            }
        }
    }
    return cookieValue;
}

const csrftoken = getCookie('csrftoken');

// ===== ALERTAS =====
function showAlert(message, type = 'success', duration = 5000) {
    const alertsContainer = document.querySelector('.alerts') || createAlertsContainer();
    
    const alert = document.createElement('div');
    alert.className = `alert alert-${type}`;
    alert.innerHTML = `
        <span>${message}</span>
        <button class="alert-close" type="button" aria-label="Close alert">
            <span aria-hidden="true">&times;</span>
        </button>
    `;
    
    alertsContainer.appendChild(alert);
    
    const closeBtn = alert.querySelector('.alert-close');
    closeBtn.addEventListener('click', () => alert.remove());
    
    if (duration) {
        setTimeout(() => alert.remove(), duration);
    }
}

function createAlertsContainer() {
    const container = document.createElement('div');
    container.className = 'alerts';
    const content = document.querySelector('.content');
    if (content) {
        content.insertBefore(container, content.firstChild);
    }
    return container;
}

// ===== API CALLS =====
async function apiCall(endpoint, method = 'GET', data = null) {
    const options = {
        method: method,
        headers: {
            'Content-Type': 'application/json',
            'X-CSRFToken': csrftoken,
        }
    };
    
    if (data && (method === 'POST' || method === 'PUT' || method === 'PATCH')) {
        options.body = JSON.stringify(data);
    }
    
    try {
        const response = await fetch(`${API_BASE_URL}${endpoint}`, options);
        
        if (!response.ok) {
            const error = await response.json();
            throw new Error(error.detail || `Error ${response.status}`);
        }
        
        if (response.status === 204) {
            return null;
        }
        
        return await response.json();
    } catch (error) {
        console.error('API Error:', error);
        showAlert(`Error: ${error.message}`, 'error');
        throw error;
    }
}

// ===== FORMULARIOS =====
function initializeFormHandlers() {
    document.querySelectorAll('form[data-api]').forEach(form => {
        form.addEventListener('submit', handleFormSubmit);
    });
}

async function handleFormSubmit(e) {
    e.preventDefault();
    
    const form = e.target;
    const endpoint = form.getAttribute('data-api');
    const method = form.getAttribute('data-method') || 'POST';
    
    try {
        showLoading(true);
        
        const formData = new FormData(form);
        const data = Object.fromEntries(formData);
        
        const response = await apiCall(endpoint, method, data);
        
        showAlert('¡Operación exitosa!', 'success');
        form.reset();
        
        // Trigger custom event for form success
        form.dispatchEvent(new CustomEvent('formSuccess', { detail: response }));
        
    } catch (error) {
        showAlert(`Error: ${error.message}`, 'error');
    } finally {
        showLoading(false);
    }
}

function showLoading(show = true) {
    let loader = document.querySelector('.loading-spinner');
    if (!loader && show) {
        loader = document.createElement('div');
        loader.className = 'loading-spinner';
        loader.innerHTML = '<div class="spinner"></div>';
        document.body.appendChild(loader);
    }
    if (loader) {
        loader.style.display = show ? 'flex' : 'none';
    }
}

// ===== TABLAS Y LISTADOS =====
function initializeTableActions() {
    document.querySelectorAll('.btn-delete').forEach(btn => {
        btn.addEventListener('click', handleDelete);
    });
    
    document.querySelectorAll('.btn-edit').forEach(btn => {
        btn.addEventListener('click', handleEdit);
    });
}

async function handleDelete(e) {
    e.preventDefault();
    
    if (!confirm('¿Estás seguro de que deseas eliminar este registro?')) {
        return;
    }
    
    const url = e.target.getAttribute('href');
    const itemId = e.target.getAttribute('data-id');
    
    try {
        await apiCall(url, 'DELETE');
        showAlert('Registro eliminado exitosamente', 'success');
        
        // Remove row from table
        const row = e.target.closest('tr');
        if (row) {
            row.remove();
        }
    } catch (error) {
        showAlert(`Error al eliminar: ${error.message}`, 'error');
    }
}

async function handleEdit(e) {
    const url = e.target.getAttribute('href');
    window.location.href = url;
}

// ===== BÚSQUEDA Y FILTRADO =====
function initializeSearch() {
    const searchInputs = document.querySelectorAll('[data-search]');
    
    searchInputs.forEach(input => {
        input.addEventListener('input', debounce(handleSearch, 300));
    });
}

function handleSearch(e) {
    const searchTerm = e.target.value.toLowerCase();
    const tableBody = document.querySelector('tbody');
    
    if (!tableBody) return;
    
    const rows = tableBody.querySelectorAll('tr');
    rows.forEach(row => {
        const text = row.textContent.toLowerCase();
        row.style.display = text.includes(searchTerm) ? '' : 'none';
    });
}

function debounce(func, wait) {
    let timeout;
    return function executedFunction(...args) {
        const later = () => {
            clearTimeout(timeout);
            func(...args);
        };
        clearTimeout(timeout);
        timeout = setTimeout(later, wait);
    };
}

// ===== SELECTORES DINÁMICOS =====
function initializeDependentSelects() {
    document.querySelectorAll('[data-depends-on]').forEach(select => {
        const dependsOn = select.getAttribute('data-depends-on');
        const dependsOnSelect = document.querySelector(`[name="${dependsOn}"]`);
        
        if (dependsOnSelect) {
            dependsOnSelect.addEventListener('change', () => {
                loadDependentOptions(select);
            });
        }
    });
}

async function loadDependentOptions(selectElement) {
    const dependsOn = selectElement.getAttribute('data-depends-on');
    const dependsOnSelect = document.querySelector(`[name="${dependsOn}"]`);
    const apiEndpoint = selectElement.getAttribute('data-api');
    
    if (!dependsOnSelect?.value || !apiEndpoint) return;
    
    try {
        const response = await apiCall(`${apiEndpoint}?${dependsOn}=${dependsOnSelect.value}`);
        
        selectElement.innerHTML = '<option value="">-- Seleccionar --</option>';
        
        if (Array.isArray(response)) {
            response.forEach(item => {
                const option = document.createElement('option');
                option.value = item.id;
                option.textContent = item.nombre || item.name || item.description;
                selectElement.appendChild(option);
            });
        }
    } catch (error) {
        console.error('Error loading options:', error);
    }
}

// ===== PAGINACIÓN =====
function initializePagination() {
    document.querySelectorAll('.pagination a').forEach(link => {
        link.addEventListener('click', handlePaginationClick);
    });
}

function handlePaginationClick(e) {
    e.preventDefault();
    const url = e.target.href;
    window.location.href = url;
}

// ===== EXPORTACIÓN DE DATOS =====
function exportToCSV(filename = 'export.csv') {
    const table = document.querySelector('table');
    if (!table) {
        showAlert('No se encontró tabla para exportar', 'error');
        return;
    }
    
    let csv = [];
    
    // Headers
    const headers = [];
    table.querySelectorAll('th').forEach(th => {
        headers.push(th.textContent.trim());
    });
    csv.push(headers.join(','));
    
    // Rows
    table.querySelectorAll('tbody tr').forEach(tr => {
        const row = [];
        tr.querySelectorAll('td').forEach(td => {
            row.push(`"${td.textContent.trim()}"`);
        });
        csv.push(row.join(','));
    });
    
    downloadFile(csv.join('\n'), filename, 'text/csv');
}

function exportToJSON(filename = 'export.json') {
    const table = document.querySelector('table');
    if (!table) {
        showAlert('No se encontró tabla para exportar', 'error');
        return;
    }
    
    const headers = [];
    table.querySelectorAll('th').forEach(th => {
        headers.push(th.textContent.trim());
    });
    
    const data = [];
    table.querySelectorAll('tbody tr').forEach(tr => {
        const row = {};
        tr.querySelectorAll('td').forEach((td, index) => {
            row[headers[index]] = td.textContent.trim();
        });
        data.push(row);
    });
    
    downloadFile(JSON.stringify(data, null, 2), filename, 'application/json');
}

function downloadFile(content, filename, type) {
    const blob = new Blob([content], { type });
    const url = URL.createObjectURL(blob);
    const a = document.createElement('a');
    a.href = url;
    a.download = filename;
    document.body.appendChild(a);
    a.click();
    document.body.removeChild(a);
    URL.revokeObjectURL(url);
}

// ===== SIDEBAR MÓVIL =====
function initializeSidebar() {
    const toggle = document.getElementById('menuToggle');
    const sidebar = document.getElementById('sidebar');
    const overlay = document.getElementById('sidebarOverlay');
    if (!toggle || !sidebar) return;

    function closeSidebar() {
        sidebar.classList.remove('show');
        if (overlay) overlay.classList.remove('show');
    }

    toggle.addEventListener('click', () => {
        sidebar.classList.toggle('show');
        if (overlay) overlay.classList.toggle('show');
    });

    if (overlay) {
        overlay.addEventListener('click', closeSidebar);
    }

    sidebar.querySelectorAll('a').forEach(link => {
        link.addEventListener('click', () => {
            if (window.innerWidth <= 768) {
                closeSidebar();
            }
        });
    });
}

// ===== CONFIRMACIÓN DE ACCIONES =====
function initializeConfirmActions() {
    document.querySelectorAll('.confirm-action').forEach(link => {
        link.addEventListener('click', function(e) {
            const msg = this.getAttribute('data-message') || '¿Está seguro de continuar?';
            if (!confirm(msg)) {
                e.preventDefault();
            }
        });
    });
}

// ===== ALERTAS MEJORADAS =====
function initializeAlerts() {
    document.querySelectorAll('.alert-close').forEach(btn => {
        btn.addEventListener('click', () => {
            const alert = btn.closest('.alert');
            if (alert) alert.remove();
        });
    });

    document.querySelectorAll('.alert').forEach(alert => {
        setTimeout(() => {
            if (alert.parentElement) {
                alert.remove();
            }
        }, 6000);
    });
}

// ===== FORMULARIOS CON ESTADO DE CARGA =====
function initializeFormLoading() {
    document.querySelectorAll('.form-submit-loading').forEach(form => {
        form.addEventListener('submit', function() {
            const btn = form.querySelector('[type="submit"]');
            if (btn && !btn.disabled) {
                btn.disabled = true;
                const icon = btn.querySelector('i');
                if (icon) {
                    icon.className = 'fa-solid fa-spinner fa-spin';
                }
                const text = btn.childNodes;
                for (const node of [...btn.childNodes]) {
                    if (node.nodeType === Node.TEXT_NODE && node.textContent.trim()) {
                        node.textContent = ' Procesando...';
                    }
                }
            }
            showLoading(true);
        });
    });
}

// ===== INICIALIZACIÓN =====
document.addEventListener('DOMContentLoaded', function() {
    initializeFormHandlers();
    initializeTableActions();
    initializeSearch();
    initializeDependentSelects();
    initializePagination();
    initializeSidebar();
    initializeConfirmActions();
    initializeAlerts();
    initializeFormLoading();
});

// ===== UTILIDADES ADICIONALES =====
function formatDate(dateString) {
    const options = { year: 'numeric', month: 'long', day: 'numeric' };
    return new Date(dateString).toLocaleDateString('es-ES', options);
}

function formatTime(dateString) {
    const options = { hour: '2-digit', minute: '2-digit' };
    return new Date(dateString).toLocaleTimeString('es-ES', options);
}

function formatDateTime(dateString) {
    return `${formatDate(dateString)} ${formatTime(dateString)}`;
}

// ===== VALIDACIÓN DE FORMULARIOS =====
function validateForm(form) {
    const requiredFields = form.querySelectorAll('[required]');
    let isValid = true;
    
    requiredFields.forEach(field => {
        if (!field.value.trim()) {
            isValid = false;
            field.classList.add('is-invalid');
        } else {
            field.classList.remove('is-invalid');
        }
    });
    
    return isValid;
}

// ===== MODAL =====
function openModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'flex';
    }
}

function closeModal(modalId) {
    const modal = document.getElementById(modalId);
    if (modal) {
        modal.style.display = 'none';
    }
}

// Modal close on background click
document.addEventListener('click', function(e) {
    if (e.target.classList.contains('modal')) {
        e.target.style.display = 'none';
    }
});

// ===== SIDEBAR TOGGLE (MOBILE) =====
function toggleSidebar() {
    const sidebar = document.querySelector('.sidebar');
    if (sidebar) {
        sidebar.classList.toggle('show');
    }
}
