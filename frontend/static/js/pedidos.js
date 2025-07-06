// Sistema de Gerenciamento de Pedidos
class PedidoManager {
    constructor(mesaId) {
        this.mesaId = mesaId;
        this.produtos = [];
        this.consumo = [];
        this.init();
    }

    init() {
        this.carregarProdutos();
        this.carregarConsumo();
        this.bindEvents();
    }

    bindEvents() {
        // Modal de adicionar pedido
        const produtoSelect = document.getElementById('produto-select');
        const quantidadeInput = document.getElementById('quantidade-input');
        
        if (produtoSelect) {
            produtoSelect.addEventListener('change', () => this.calcularTotal());
        }
        
        if (quantidadeInput) {
            quantidadeInput.addEventListener('input', () => this.calcularTotal());
        }
    }

    async carregarProdutos() {
        try {
            const response = await fetch('/api/produtos/');
            if (response.ok) {
                this.produtos = await response.json();
                this.atualizarSelectProdutos();
            }
        } catch (error) {
            console.error('Erro ao carregar produtos:', error);
            this.mostrarNotificacao('Erro ao carregar produtos', 'error');
        }
    }

    async carregarConsumo() {
        try {
            const response = await fetch(`/api/consumo/${this.mesaId}/`);
            if (response.ok) {
                this.consumo = await response.json();
                this.renderizarConsumo();
            }
        } catch (error) {
            console.error('Erro ao carregar consumo:', error);
            this.mostrarNotificacao('Erro ao carregar consumo da mesa', 'error');
        }
    }

    atualizarSelectProdutos() {
        const select = document.getElementById('produto-select');
        if (!select) return;

        select.innerHTML = '<option value="">Selecione um produto...</option>';
        
        this.produtos.forEach(produto => {
            const option = document.createElement('option');
            option.value = produto.id;
            option.dataset.preco = produto.preco;
            option.textContent = `${produto.nome} - R$ ${this.formatarMoeda(produto.preco)}`;
            select.appendChild(option);
        });
    }

    renderizarConsumo() {
        const container = document.querySelector('.card-body');
        if (!container) return;

        // Limpar container existente - remover todos os elementos dinâmicos
        const consumoItems = container.querySelectorAll('.consumo-item');
        consumoItems.forEach(item => item.remove());

        // Remover elementos de consumo vazio criados dinamicamente
        const emptyDivs = container.querySelectorAll('.text-center.py-4:not(#consumo-vazio)');
        emptyDivs.forEach(div => div.remove());

        if (this.consumo.length === 0) {
            this.mostrarConsumoVazio(container);
            return;
        }

        // Esconder o elemento de consumo vazio do template
        const consumoVazioTemplate = document.getElementById('consumo-vazio');
        if (consumoVazioTemplate) {
            consumoVazioTemplate.style.display = 'none';
        }

        this.consumo.forEach(item => {
            const itemElement = this.criarElementoConsumo(item);
            container.appendChild(itemElement);
        });

        this.atualizarTotalGeral();
    }

    criarElementoConsumo(item) {
        const div = document.createElement('div');
        div.className = 'consumo-item';
        div.innerHTML = `
            <div class="row align-items-center">
                <div class="col-md-6">
                    <h6 class="mb-1">${item.nome}</h6>
                    <small class="text-muted">R$ ${this.formatarMoeda(item.preco)} cada</small>
                </div>
                <div class="col-md-3 text-center">
                    <span class="badge bg-primary">Qtd: ${item.quantidade}</span>
                </div>
                <div class="col-md-3 text-end">
                    <div class="d-flex justify-content-end action-buttons">
                        <strong class="text-success me-2">R$ ${this.formatarMoeda(item.total)}</strong>
                        <button class="btn btn-warning btn-sm btn-action" 
                                onclick="pedidoManager.abrirModalPagarItem(${item.id}, '${item.nome}', ${item.total})">
                            <i class="bi bi-credit-card"></i>
                        </button>
                        <button class="btn btn-danger btn-sm btn-action" 
                                onclick="pedidoManager.abrirModalAbaterItem(${item.id}, '${item.nome}', ${item.quantidade})">
                            <i class="bi bi-dash-circle"></i>
                        </button>
                    </div>
                </div>
            </div>
        `;
        return div;
    }

    mostrarConsumoVazio(container) {
        // Usar o elemento existente do template
        const consumoVazioTemplate = document.getElementById('consumo-vazio');
        if (consumoVazioTemplate) {
            consumoVazioTemplate.style.display = 'block';

            // Adicionar o botão se não existir
            if (!consumoVazioTemplate.querySelector('button')) {
                const button = document.createElement('button');
                button.className = 'btn btn-primary';
                button.onclick = abrirModalAdicionarPedido;
                button.innerHTML = '<i class="bi bi-plus-circle"></i> Adicionar Primeiro Pedido';
                consumoVazioTemplate.appendChild(button);
            }
        }
    }

    calcularTotal() {
        const select = document.getElementById('produto-select');
        const quantidadeInput = document.getElementById('quantidade-input');
        const totalPreview = document.getElementById('total-preview');
        
        if (!select || !quantidadeInput || !totalPreview) return;

        const selectedOption = select.options[select.selectedIndex];
        const preco = selectedOption ? parseFloat(selectedOption.dataset.preco) || 0 : 0;
        const quantidade = parseInt(quantidadeInput.value) || 0;
        const total = preco * quantidade;

        totalPreview.value = `R$ ${this.formatarMoeda(total)}`;
    }

    async adicionarPedido() {
        const produtoId = document.getElementById('produto-select')?.value;
        const quantidade = parseInt(document.getElementById('quantidade-input')?.value);

        if (!produtoId || !quantidade) {
            this.mostrarNotificacao('Por favor, selecione um produto e informe a quantidade.', 'warning');
            return;
        }

        try {
            const response = await fetch('/api/adicionar-pedido/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({
                    produto_id: parseInt(produtoId),
                    quantidade: quantidade,
                    mesa_id: this.mesaId
                })
            });

            if (response.ok) {
                this.mostrarNotificacao('Pedido adicionado com sucesso!', 'success');
                this.carregarConsumo();
                this.fecharModal('modalAdicionarPedido');
                this.limparFormulario();
            } else {
                const error = await response.json();
                this.mostrarNotificacao(error.detail || 'Erro ao adicionar pedido', 'error');
            }
        } catch (error) {
            console.error('Erro ao adicionar pedido:', error);
            this.mostrarNotificacao('Erro ao adicionar pedido', 'error');
        }
    }

    async abaterConsumo(consumoId, quantidade) {
        try {
            const response = await fetch('/api/abater-consumo/', {
                method: 'POST',
                headers: {
                    'Content-Type': 'application/json',
                    'X-CSRFToken': this.getCsrfToken()
                },
                body: JSON.stringify({
                    consumo_id: consumoId,
                    mesa_id: this.mesaId,
                    quantidade: quantidade
                })
            });

            if (response.ok) {
                this.mostrarNotificacao('Item atualizado com sucesso!', 'success');
                this.carregarConsumo();
            } else {
                const error = await response.json();
                this.mostrarNotificacao(error.detail || 'Erro ao atualizar item', 'error');
            }
        } catch (error) {
            console.error('Erro ao abater consumo:', error);
            this.mostrarNotificacao('Erro ao atualizar item', 'error');
        }
    }

    abrirModalPagarItem(itemId, nome, total) {
        const confirmar = confirm(
            `Confirma o pagamento do item "${nome}" no valor de R$ ${this.formatarMoeda(total)}?`
        );
        
        if (confirmar) {
            // Por enquanto, apenas simula o pagamento removendo o item
            this.abaterConsumo(itemId, 999); // Quantidade alta para remover completamente
        }
    }

    abrirModalAbaterItem(itemId, nome, quantidadeAtual) {
        const quantidade = prompt(
            `Quantos itens de "${nome}" deseja abater?\n(Quantidade atual: ${quantidadeAtual})`,
            '1'
        );
        
        if (quantidade && !isNaN(quantidade)) {
            const qtd = parseInt(quantidade);
            if (qtd > 0 && qtd <= quantidadeAtual) {
                this.abaterConsumo(itemId, qtd);
            } else {
                this.mostrarNotificacao('Quantidade inválida', 'warning');
            }
        }
    }

    atualizarTotalGeral() {
        const total = this.consumo.reduce((sum, item) => sum + (item.total || 0), 0);
        const totalElement = document.querySelector('.total-section h2');
        if (totalElement) {
            totalElement.textContent = `R$ ${this.formatarMoeda(total)}`;
        }
    }

    limparFormulario() {
        const produtoSelect = document.getElementById('produto-select');
        const quantidadeInput = document.getElementById('quantidade-input');
        const totalPreview = document.getElementById('total-preview');
        
        if (produtoSelect) produtoSelect.value = '';
        if (quantidadeInput) quantidadeInput.value = '1';
        if (totalPreview) totalPreview.value = '';
    }

    fecharModal(modalId) {
        const modal = document.getElementById(modalId);
        if (modal) {
            const bsModal = bootstrap.Modal.getInstance(modal);
            if (bsModal) {
                bsModal.hide();
            }
        }
    }

    formatarMoeda(valor) {
        return valor.toFixed(2).replace('.', ',');
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

    mostrarNotificacao(mensagem, tipo = 'info') {
        const notification = document.createElement('div');
        notification.className = `alert alert-${tipo === 'error' ? 'danger' : tipo} alert-dismissible fade show position-fixed`;
        notification.style.cssText = 'top: 20px; right: 20px; z-index: 9999; min-width: 300px;';
        notification.innerHTML = `
            ${mensagem}
            <button type="button" class="btn-close" data-bs-dismiss="alert"></button>
        `;

        document.body.appendChild(notification);

        setTimeout(() => {
            if (notification.parentNode) {
                notification.parentNode.removeChild(notification);
            }
        }, 5000);
    }
}

// Funções globais para os templates
function abrirModalAdicionarPedido() {
    const modal = new bootstrap.Modal(document.getElementById('modalAdicionarPedido'));
    modal.show();
}

function adicionarPedido() {
    if (window.pedidoManager) {
        window.pedidoManager.adicionarPedido();
    }
}

// Funções para as ações da mesa
function abrirModalFinalizarConta() {
    const modal = new bootstrap.Modal(document.getElementById('modalFinalizarConta'));
    modal.show();
}

function abrirModalEditarMesa() {
    const modal = new bootstrap.Modal(document.getElementById('modalEditarMesa'));
    modal.show();
}

function imprimirConta() {
    // Criar uma nova janela para impressão
    const printWindow = window.open('', '_blank', 'width=800,height=600');

    // Obter dados da mesa
    const mesaId = document.querySelector('[data-mesa-id]')?.dataset.mesaId;
    const mesaNome = document.querySelector('h1').textContent.trim();
    const cliente = document.querySelector('[data-mesa-id]')?.dataset.cliente || 'Cliente não informado';

    // Obter itens do consumo
    const consumoItems = window.pedidoManager ? window.pedidoManager.consumo : [];
    const total = consumoItems.reduce((sum, item) => sum + (item.total || 0), 0);

    // HTML para impressão
    const printHTML = `
        <!DOCTYPE html>
        <html>
        <head>
            <title>Conta - ${mesaNome}</title>
            <style>
                body {
                    font-family: 'Courier New', monospace;
                    margin: 20px;
                    font-size: 12px;
                    line-height: 1.4;
                }
                .header {
                    text-align: center;
                    border-bottom: 2px solid #000;
                    padding-bottom: 10px;
                    margin-bottom: 20px;
                }
                .logo {
                    font-size: 18px;
                    font-weight: bold;
                    margin-bottom: 5px;
                }
                .info {
                    margin-bottom: 20px;
                }
                .item {
                    display: flex;
                    justify-content: space-between;
                    margin-bottom: 5px;
                    border-bottom: 1px dotted #ccc;
                    padding-bottom: 3px;
                }
                .total {
                    border-top: 2px solid #000;
                    padding-top: 10px;
                    margin-top: 20px;
                    font-weight: bold;
                    font-size: 14px;
                }
                .footer {
                    text-align: center;
                    margin-top: 30px;
                    border-top: 1px solid #000;
                    padding-top: 10px;
                    font-size: 10px;
                }
                @media print {
                    body { margin: 0; }
                    .no-print { display: none; }
                }
            </style>
        </head>
        <body>
            <div class="header">
                <div class="logo">ALTO DA SERRA</div>
                <div>Restaurante e Lanchonete</div>
                <div>Tel: (11) 99999-9999</div>
            </div>

            <div class="info">
                <div><strong>Mesa:</strong> ${mesaNome}</div>
                <div><strong>Cliente:</strong> ${cliente}</div>
                <div><strong>Data:</strong> ${new Date().toLocaleDateString('pt-BR')}</div>
                <div><strong>Hora:</strong> ${new Date().toLocaleTimeString('pt-BR')}</div>
            </div>

            <div class="items">
                <div style="font-weight: bold; margin-bottom: 10px;">ITENS CONSUMIDOS:</div>
                ${consumoItems.map(item => `
                    <div class="item">
                        <div>${item.quantidade}x ${item.nome}</div>
                        <div>R$ ${item.total.toFixed(2).replace('.', ',')}</div>
                    </div>
                `).join('')}
            </div>

            <div class="total">
                <div style="display: flex; justify-content: space-between;">
                    <div>TOTAL GERAL:</div>
                    <div>R$ ${total.toFixed(2).replace('.', ',')}</div>
                </div>
            </div>

            <div class="footer">
                <div>Obrigado pela preferência!</div>
                <div>Volte sempre!</div>
            </div>

            <div class="no-print" style="text-align: center; margin-top: 20px;">
                <button onclick="window.print()" style="padding: 10px 20px; font-size: 14px;">
                    Imprimir Conta
                </button>
                <button onclick="window.close()" style="padding: 10px 20px; font-size: 14px; margin-left: 10px;">
                    Fechar
                </button>
            </div>
        </body>
        </html>
    `;

    printWindow.document.write(printHTML);
    printWindow.document.close();

    // Auto-imprimir após carregar
    printWindow.onload = function() {
        setTimeout(() => {
            printWindow.print();
        }, 500);
    };
}

async function confirmarFinalizacao() {
    const formaPagamento = document.getElementById('forma-pagamento')?.value;
    const valorPago = parseFloat(document.getElementById('valor-pago')?.value) || 0;
    const observacoes = document.getElementById('observacoes-pagamento')?.value || '';

    if (!formaPagamento) {
        alert('Por favor, selecione a forma de pagamento.');
        return;
    }

    const total = window.pedidoManager ?
        window.pedidoManager.consumo.reduce((sum, item) => sum + (item.total || 0), 0) : 0;

    if (valorPago < total) {
        const confirmar = confirm(`Valor pago (R$ ${valorPago.toFixed(2)}) é menor que o total (R$ ${total.toFixed(2)}). Deseja continuar?`);
        if (!confirmar) return;
    }

    try {
        // Obter mesa_id da URL
        const urlParts = window.location.pathname.split('/');
        const mesaId = urlParts[urlParts.length - 2]; // Pega o penúltimo elemento (antes da barra final)

        const response = await fetch('/api/finalizar-conta/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify({
                mesa_id: mesaId, // Manter como string
                forma_pagamento: formaPagamento,
                valor_pago: valorPago,
                observacoes: observacoes,
                total: total
            })
        });

        if (response.ok) {
            alert('Conta finalizada com sucesso!');

            // Fechar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('modalFinalizarConta'));
            if (modal) modal.hide();

            // Redirecionar para dashboard
            window.location.href = '/dashboard/';
        } else {
            const error = await response.json();
            alert(error.detail || 'Erro ao finalizar conta');
        }
    } catch (error) {
        console.error('Erro ao finalizar conta:', error);
        alert('Erro ao finalizar conta');
    }
}

async function salvarEdicaoMesa() {
    const cliente = document.getElementById('cliente-nome')?.value || '';
    const cpfCnpj = document.getElementById('cliente-cpf')?.value || '';

    try {
        // Obter mesa_id da URL
        const urlParts = window.location.pathname.split('/');
        const mesaId = urlParts[urlParts.length - 2]; // Pega o penúltimo elemento (antes da barra final)

        const requestData = {
            mesa_id: mesaId, // Manter como string, pois no backend é string
            cliente: cliente,
            cpf_cnpj: cpfCnpj
        };

        const response = await fetch('/api/editar-mesa/', {
            method: 'POST',
            headers: {
                'Content-Type': 'application/json',
                'X-CSRFToken': getCsrfToken()
            },
            body: JSON.stringify(requestData)
        });

        if (response.ok) {
            alert('Mesa atualizada com sucesso!');

            // Fechar modal
            const modal = bootstrap.Modal.getInstance(document.getElementById('modalEditarMesa'));
            if (modal) modal.hide();

            // Recarregar página para mostrar as alterações
            window.location.reload();
        } else {
            const error = await response.json();
            alert(error.detail || 'Erro ao atualizar mesa');
        }
    } catch (error) {
        console.error('Erro ao atualizar mesa:', error);
        alert('Erro ao atualizar mesa');
    }
}

function getCsrfToken() {
    const cookies = document.cookie.split(';');
    for (let cookie of cookies) {
        const [name, value] = cookie.trim().split('=');
        if (name === 'csrftoken') {
            return value;
        }
    }
    return '';
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    const mesaId = document.querySelector('[data-mesa-id]')?.dataset.mesaId;
    if (mesaId) {
        window.pedidoManager = new PedidoManager(mesaId);
    }
});
