// Dashboard JavaScript Functions
class MesaManager {
    constructor() {
        this.mesas = [];
        this.filtros = {
            mesa: '',
            cliente: '',
            status: ''
        };
        this.init();
    }

    init() {
        this.bindEvents();
        this.carregarMesas();
        this.atualizarEstatisticas();
    }

    bindEvents() {
        // Filtros
        document.getElementById('filtro-mesa')?.addEventListener('input', (e) => {
            this.filtros.mesa = e.target.value.toLowerCase();
            this.aplicarFiltros();
        });

        document.getElementById('filtro-cliente')?.addEventListener('input', (e) => {
            this.filtros.cliente = e.target.value.toLowerCase();
            this.aplicarFiltros();
        });

        document.getElementById('filtro-status')?.addEventListener('change', (e) => {
            this.filtros.status = e.target.value.toLowerCase();
            this.aplicarFiltros();
        });

        // Auto-refresh a cada 30 segundos
        setInterval(() => {
            this.carregarMesas();
        }, 30000);
    }

    async carregarMesas() {
        try {
            const response = await fetch('/api/mesas/');
            if (response.ok) {
                this.mesas = await response.json();
                this.renderizarMesas();
                this.atualizarEstatisticas();
            }
        } catch (error) {
            console.error('Erro ao carregar mesas:', error);
            this.mostrarNotificacao('Erro ao carregar dados das mesas', 'error');
        }
    }

    renderizarMesas() {
        const container = document.getElementById('mesas-container');
        if (!container) return;

        container.innerHTML = '';

        this.mesas.forEach(mesa => {
            const mesaElement = this.criarElementoMesa(mesa);
            container.appendChild(mesaElement);
        });

        this.aplicarFiltros();
    }

    criarElementoMesa(mesa) {
        const div = document.createElement('div');
        div.className = 'col-lg-3 col-md-4 col-sm-6 mesa-item';
        div.dataset.mesaId = mesa.id;
        div.dataset.cliente = (mesa.cliente || '').toLowerCase();
        div.dataset.status = (mesa.status || '').toLowerCase();

        const statusClass = this.getStatusClass(mesa.status);
        const statusBadgeClass = this.getStatusBadgeClass(mesa.status);

        div.innerHTML = `
            <div class="card mesa-card" onclick="abrirDetalheMesa('${mesa.id}')">
                <div class="card-body">
                    <div class="d-flex justify-content-between align-items-start mb-2">
                        <h5 class="card-title mb-0">${mesa.nome || mesa.id}</h5>
                        <span class="status-badge ${statusBadgeClass}">
                            ${mesa.status ? mesa.status.charAt(0).toUpperCase() + mesa.status.slice(1) : 'N/A'}
                        </span>
                    </div>
                    
                    ${mesa.cliente ? `
                        <p class="card-text">
                            <i class="bi bi-person"></i> ${mesa.cliente}
                        </p>
                    ` : ''}
                    
                    ${mesa.cpf_cnpj ? `
                        <p class="card-text">
                            <i class="bi bi-card-text"></i> ${mesa.cpf_cnpj}
                        </p>
                    ` : ''}
                    
                    <div class="d-flex justify-content-between align-items-center">
                        <small class="text-muted">${mesa.id}</small>
                        <strong class="text-success">R$ ${this.formatarMoeda(mesa.total || 0)}</strong>
                    </div>
                </div>
            </div>
        `;

        return div;
    }

    getStatusClass(status) {
        const statusMap = {
            'livre': 'status-livre',
            'ocupada': 'status-ocupada',
            'reservada': 'status-reservada'
        };
        return statusMap[status?.toLowerCase()] || '';
    }

    getStatusBadgeClass(status) {
        const statusMap = {
            'livre': 'status-livre',
            'ocupada': 'status-ocupada',
            'reservada': 'status-reservada'
        };
        return statusMap[status?.toLowerCase()] || 'bg-secondary';
    }

    aplicarFiltros() {
        const mesaItems = document.querySelectorAll('.mesa-item');
        
        mesaItems.forEach(item => {
            const mesaId = item.dataset.mesaId.toLowerCase();
            const cliente = item.dataset.cliente;
            const status = item.dataset.status;

            const mostrar = 
                (!this.filtros.mesa || mesaId.includes(this.filtros.mesa)) &&
                (!this.filtros.cliente || cliente.includes(this.filtros.cliente)) &&
                (!this.filtros.status || status === this.filtros.status);

            item.style.display = mostrar ? 'block' : 'none';
        });
    }

    atualizarEstatisticas() {
        const mesasVisiveis = document.querySelectorAll('.mesa-item[style="display: block"], .mesa-item:not([style])');
        let ocupadas = 0, livres = 0, reservadas = 0, faturamento = 0;

        mesasVisiveis.forEach(mesa => {
            const status = mesa.dataset.status;
            const valorElement = mesa.querySelector('.text-success');
            const valor = valorElement ? 
                parseFloat(valorElement.textContent.replace('R$ ', '').replace(',', '.')) || 0 : 0;

            switch(status) {
                case 'ocupada': ocupadas++; break;
                case 'livre': livres++; break;
                case 'reservada': reservadas++; break;
            }

            faturamento += valor;
        });

        // Atualizar elementos da interface
        this.atualizarElemento('total-mesas', mesasVisiveis.length);
        this.atualizarElemento('mesas-ocupadas', ocupadas);
        this.atualizarElemento('mesas-livres', livres);
        this.atualizarElemento('faturamento-total', `R$ ${this.formatarMoeda(faturamento)}`);
    }

    atualizarElemento(id, valor) {
        const elemento = document.getElementById(id);
        if (elemento) {
            elemento.textContent = valor;
        }
    }

    formatarMoeda(valor) {
        return valor.toFixed(2).replace('.', ',');
    }

    mostrarNotificacao(mensagem, tipo = 'info') {
        // Criar elemento de notificação
        const notification = document.createElement('div');
        notification.className = `alert alert-${tipo === 'error' ? 'danger' : tipo} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${mensagem}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        // Remover após 5 segundos
        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }

    async atualizarStatusMesa(mesaId, novoStatus, cliente = '') {
        try {
            const response = await fetch('/api/atualizar-mesa/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({
                    id: mesaId.replace('M', ''),
                    status: novoStatus,
                    cliente: cliente,
                    user_id: 'admin' // Pegar do contexto do usuário
                })
            });

            if (response.ok) {
                this.mostrarNotificacao('Mesa atualizada com sucesso!', 'success');
                this.carregarMesas();
            } else {
                const error = await response.json();
                this.mostrarNotificacao(error.detail || 'Erro ao atualizar mesa', 'error');
            }
        } catch (error) {
            console.error('Erro ao atualizar mesa:', error);
            this.mostrarNotificacao('Erro ao atualizar mesa', 'error');
        }
    }

    getCsrfToken() {
        const cookies = document.cookie.split(';');
        for (let cookie of cookies) {
            const [name, value] = cookie.trim().split('=');
            if (name === 'csrftoken') {
                return value;
            }
        }
        return '';
    }
}

// Funções globais
function abrirDetalheMesa(mesaId) {
    window.location.href = `/mesa/${mesaId}/`;
}

function refreshData() {
    if (window.mesaManager) {
        window.mesaManager.carregarMesas();
    } else {
        location.reload();
    }
}

function aplicarFiltros() {
    if (window.mesaManager) {
        window.mesaManager.aplicarFiltros();
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    window.mesaManager = new MesaManager();
});
