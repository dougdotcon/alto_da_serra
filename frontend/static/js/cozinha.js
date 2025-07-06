class CozinhaManager {
    constructor() {
        this.pedidos = [];
        this.pedidoSelecionado = null;
        this.init();
    }

    init() {
        this.carregarPedidos();
        this.configurarEventos();
        // Atualizar automaticamente a cada 30 segundos
        setInterval(() => this.carregarPedidos(), 30000);
    }

    configurarEventos() {
        // Configurar eventos se necessário
    }

    async carregarPedidos() {
        try {
            this.mostrarLoading(true);
            
            // Buscar todas as mesas com pedidos
            const mesasResponse = await fetch('/api/mesas/');
            if (mesasResponse.ok) {
                const mesas = await mesasResponse.json();
                
                // Buscar consumo de cada mesa ocupada
                const pedidosPromises = mesas
                    .filter(mesa => mesa.status.toLowerCase() === 'aberto')
                    .map(async mesa => {
                        try {
                            const consumoResponse = await fetch(`/api/consumo/${mesa.id}/`);
                            if (consumoResponse.ok) {
                                const consumo = await consumoResponse.json();
                                if (consumo.length > 0) {
                                    return {
                                        mesa: mesa,
                                        itens: consumo,
                                        status: this.determinarStatusPedido(mesa, consumo),
                                        tempo: this.calcularTempoPedido(mesa)
                                    };
                                }
                            }
                        } catch (error) {
                            console.error(`Erro ao carregar consumo da mesa ${mesa.id}:`, error);
                        }
                        return null;
                    });
                
                const pedidosResolvidos = await Promise.all(pedidosPromises);
                this.pedidos = pedidosResolvidos.filter(pedido => pedido !== null);
                
                this.renderizarPedidos();
                this.atualizarEstatisticas();
            } else {
                this.mostrarErro('Erro ao carregar pedidos');
            }
        } catch (error) {
            console.error('Erro ao carregar pedidos:', error);
            this.mostrarErro('Erro ao conectar com o servidor');
        } finally {
            this.mostrarLoading(false);
        }
    }

    determinarStatusPedido(mesa, consumo) {
        // Simular status baseado em dados disponíveis
        // Em um sistema real, isso viria do backend
        const agora = new Date();
        const abertura = mesa.data_abertura ? new Date(mesa.data_abertura) : agora;
        const tempoDecorrido = (agora - abertura) / (1000 * 60); // em minutos
        
        if (tempoDecorrido < 5) {
            return 'pendente';
        } else if (tempoDecorrido < 15) {
            return 'preparo';
        } else {
            return 'pronto';
        }
    }

    calcularTempoPedido(mesa) {
        const agora = new Date();
        const abertura = mesa.data_abertura ? new Date(mesa.data_abertura) : agora;
        const tempoDecorrido = Math.floor((agora - abertura) / (1000 * 60)); // em minutos
        return Math.max(0, tempoDecorrido);
    }

    renderizarPedidos() {
        const pendentesContainer = document.getElementById('pedidos-pendentes');
        const preparoContainer = document.getElementById('pedidos-preparo');
        const prontosContainer = document.getElementById('pedidos-prontos');
        
        // Limpar containers
        pendentesContainer.innerHTML = '';
        preparoContainer.innerHTML = '';
        prontosContainer.innerHTML = '';
        
        if (this.pedidos.length === 0) {
            document.getElementById('sem-pedidos').style.display = 'block';
            return;
        }
        
        document.getElementById('sem-pedidos').style.display = 'none';
        
        // Separar pedidos por status
        const pendentes = this.pedidos.filter(p => p.status === 'pendente');
        const preparo = this.pedidos.filter(p => p.status === 'preparo');
        const prontos = this.pedidos.filter(p => p.status === 'pronto');
        
        // Renderizar cada categoria
        this.renderizarCategoria(pendentes, pendentesContainer, 'pendente');
        this.renderizarCategoria(preparo, preparoContainer, 'preparo');
        this.renderizarCategoria(prontos, prontosContainer, 'pronto');
    }

    renderizarCategoria(pedidos, container, status) {
        if (pedidos.length === 0) {
            container.innerHTML = `
                <div class="text-center text-muted py-4">
                    <i class="bi bi-inbox display-4"></i>
                    <p class="mt-2">Nenhum pedido ${status}</p>
                </div>
            `;
            return;
        }
        
        container.innerHTML = pedidos.map(pedido => this.criarCardPedido(pedido, status)).join('');
    }

    criarCardPedido(pedido, status) {
        const statusText = {
            'pendente': 'Pendente',
            'preparo': 'Em Preparo',
            'pronto': 'Pronto'
        }[status];

        const itensHtml = pedido.itens.slice(0, 3).map(item => `
            <div class="item-pedido">
                <div class="item-nome">${item.produto_nome}</div>
                <div class="item-quantidade">${item.quantidade}x</div>
            </div>
        `).join('');

        const maisItens = pedido.itens.length > 3 ? `
            <div class="text-center text-muted small mt-2">
                <i class="bi bi-plus-circle"></i> +${pedido.itens.length - 3} item(ns) adicional(is)
            </div>
        ` : '';

        const acoesBotoes = this.criarBotoesPedido(pedido, status);

        return `
            <div class="pedido-card">
                <div class="pedido-header">
                    <div class="pedido-mesa">
                        <i class="bi bi-table me-2"></i>${pedido.mesa.nome}
                    </div>
                    <div class="tempo-pedido">
                        <i class="bi bi-clock me-1"></i>${pedido.tempo} min
                    </div>
                </div>

                <div class="mb-3">
                    <div class="small text-muted mb-2">
                        <i class="bi bi-person me-1"></i>${pedido.mesa.cliente || 'Cliente não informado'}
                    </div>
                    ${itensHtml}
                    ${maisItens}
                </div>

                <div class="text-center mb-3">
                    <strong class="text-primary">Total: R$ ${this.formatarMoeda(pedido.itens.reduce((sum, item) => sum + (item.preco_unitario * item.quantidade), 0))}</strong>
                </div>

                <div class="text-center">
                    ${acoesBotoes}
                </div>
            </div>
        `;
    }

    criarBotoesPedido(pedido, status) {
        const mesaId = pedido.mesa.id;

        switch (status) {
            case 'pendente':
                return `
                    <button class="btn-acao btn-iniciar" onclick="cozinhaManager.iniciarPreparo('${mesaId}')">
                        <i class="bi bi-play me-1"></i>Iniciar Preparo
                    </button>
                    <button class="btn btn-outline-primary btn-sm" onclick="cozinhaManager.verDetalhes('${mesaId}')">
                        <i class="bi bi-eye me-1"></i>Detalhes
                    </button>
                `;
            case 'preparo':
                return `
                    <button class="btn-acao btn-finalizar" onclick="cozinhaManager.marcarPronto('${mesaId}')">
                        <i class="bi bi-check me-1"></i>Marcar Pronto
                    </button>
                    <button class="btn btn-outline-primary btn-sm" onclick="cozinhaManager.verDetalhes('${mesaId}')">
                        <i class="bi bi-eye me-1"></i>Detalhes
                    </button>
                `;
            case 'pronto':
                return `
                    <button class="btn-acao btn-entregar" onclick="cozinhaManager.entregarPedido('${mesaId}')">
                        <i class="bi bi-truck me-1"></i>Entregar
                    </button>
                    <button class="btn btn-outline-primary btn-sm" onclick="cozinhaManager.verDetalhes('${mesaId}')">
                        <i class="bi bi-eye me-1"></i>Detalhes
                    </button>
                `;
            default:
                return '';
        }
    }

    atualizarEstatisticas() {
        const pendentes = this.pedidos.filter(p => p.status === 'pendente').length;
        const preparo = this.pedidos.filter(p => p.status === 'preparo').length;
        const prontos = this.pedidos.filter(p => p.status === 'pronto').length;
        
        const tempoMedio = this.pedidos.length > 0 
            ? Math.round(this.pedidos.reduce((sum, p) => sum + p.tempo, 0) / this.pedidos.length)
            : 0;
        
        document.getElementById('total-pendentes').textContent = pendentes;
        document.getElementById('total-preparo').textContent = preparo;
        document.getElementById('total-prontos').textContent = prontos;
        document.getElementById('tempo-medio').textContent = `${tempoMedio}min`;
    }

    // Métodos de ação
    iniciarPreparo(mesaId) {
        // Simular mudança de status
        const pedido = this.pedidos.find(p => p.mesa.id == mesaId);
        if (pedido) {
            pedido.status = 'preparo';
            this.renderizarPedidos();
            this.atualizarEstatisticas();
            this.mostrarNotificacao(`Preparo iniciado para ${pedido.mesa.nome}`, 'success');
        }
    }

    marcarPronto(mesaId) {
        // Simular mudança de status
        const pedido = this.pedidos.find(p => p.mesa.id == mesaId);
        if (pedido) {
            pedido.status = 'pronto';
            this.renderizarPedidos();
            this.atualizarEstatisticas();
            this.mostrarNotificacao(`${pedido.mesa.nome} está pronto!`, 'success');
        }
    }

    entregarPedido(mesaId) {
        // Simular entrega (remover da cozinha)
        this.pedidos = this.pedidos.filter(p => p.mesa.id != mesaId);
        this.renderizarPedidos();
        this.atualizarEstatisticas();
        this.mostrarNotificacao('Pedido entregue!', 'success');
    }

    verDetalhes(mesaId) {
        const pedido = this.pedidos.find(p => p.mesa.id == mesaId);
        if (pedido) {
            this.pedidoSelecionado = pedido;
            this.mostrarModalDetalhes(pedido);
        }
    }

    mostrarModalDetalhes(pedido) {
        const modalBody = document.getElementById('modal-body-detalhes');
        
        const itensHtml = pedido.itens.map(item => `
            <div class="row border-bottom py-2">
                <div class="col-1 text-center">
                    <strong>${item.quantidade}x</strong>
                </div>
                <div class="col-7">
                    ${item.produto_nome}
                </div>
                <div class="col-2 text-end">
                    R$ ${this.formatarMoeda(item.preco_unitario)}
                </div>
                <div class="col-2 text-end">
                    <strong>R$ ${this.formatarMoeda(item.preco_unitario * item.quantidade)}</strong>
                </div>
            </div>
        `).join('');
        
        const total = pedido.itens.reduce((sum, item) => sum + (item.preco_unitario * item.quantidade), 0);
        
        modalBody.innerHTML = `
            <div class="mesa-info mb-3">
                <h5><i class="bi bi-table"></i> ${pedido.mesa.nome}</h5>
                <p class="mb-1"><i class="bi bi-person"></i> Cliente: ${pedido.mesa.cliente || 'Não informado'}</p>
                <p class="mb-0"><i class="bi bi-clock"></i> Tempo: ${pedido.tempo} minutos</p>
            </div>
            
            <h6>Itens do Pedido:</h6>
            <div class="container-fluid">
                <div class="row border-bottom fw-bold py-2">
                    <div class="col-1">Qtd</div>
                    <div class="col-7">Produto</div>
                    <div class="col-2 text-end">Preço Unit.</div>
                    <div class="col-2 text-end">Subtotal</div>
                </div>
                ${itensHtml}
                <div class="row py-3">
                    <div class="col-8"></div>
                    <div class="col-4 text-end">
                        <h5>Total: R$ ${this.formatarMoeda(total)}</h5>
                    </div>
                </div>
            </div>
        `;
        
        const modal = new bootstrap.Modal(document.getElementById('modalDetalhesPedido'));
        modal.show();
    }

    mostrarLoading(mostrar) {
        document.getElementById('loading').style.display = mostrar ? 'block' : 'none';
    }

    mostrarErro(mensagem) {
        console.error(mensagem);
        this.mostrarNotificacao(mensagem, 'error');
    }

    mostrarNotificacao(mensagem, tipo) {
        // Implementar sistema de notificações
        console.log(`${tipo.toUpperCase()}: ${mensagem}`);
        // Temporário - usar alert
        if (tipo === 'error') {
            alert(`Erro: ${mensagem}`);
        }
    }

    formatarMoeda(valor) {
        return parseFloat(valor).toFixed(2).replace('.', ',');
    }

    atualizarPedidos() {
        this.carregarPedidos();
    }

    marcarTodosProntos() {
        if (confirm('Marcar todos os pedidos como prontos?')) {
            this.pedidos.forEach(pedido => {
                if (pedido.status !== 'pronto') {
                    pedido.status = 'pronto';
                }
            });
            this.renderizarPedidos();
            this.atualizarEstatisticas();
            this.mostrarNotificacao('Todos os pedidos marcados como prontos!', 'success');
        }
    }
}

// Funções globais
function atualizarPedidos() {
    if (window.cozinhaManager) {
        window.cozinhaManager.atualizarPedidos();
    }
}

function marcarTodosProntos() {
    if (window.cozinhaManager) {
        window.cozinhaManager.marcarTodosProntos();
    }
}

function iniciarPreparo() {
    if (window.cozinhaManager && window.cozinhaManager.pedidoSelecionado) {
        window.cozinhaManager.iniciarPreparo(window.cozinhaManager.pedidoSelecionado.mesa.id);
        bootstrap.Modal.getInstance(document.getElementById('modalDetalhesPedido')).hide();
    }
}

function marcarPronto() {
    if (window.cozinhaManager && window.cozinhaManager.pedidoSelecionado) {
        window.cozinhaManager.marcarPronto(window.cozinhaManager.pedidoSelecionado.mesa.id);
        bootstrap.Modal.getInstance(document.getElementById('modalDetalhesPedido')).hide();
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    window.cozinhaManager = new CozinhaManager();
});
