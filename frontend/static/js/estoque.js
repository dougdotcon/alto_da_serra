class EstoqueManager {
    constructor() {
        this.produtos = [];
        this.produtosFiltrados = [];
        this.init();
    }

    init() {
        this.carregarProdutos();
        this.configurarEventos();
    }

    configurarEventos() {
        // Configurar eventos de filtro e busca
        document.getElementById('busca-produto').addEventListener('input', () => this.filtrarProdutos());
        document.getElementById('filtro-status').addEventListener('change', () => this.filtrarProdutos());
        document.getElementById('ordenar-por').addEventListener('change', () => this.ordenarProdutos());
    }

    async carregarProdutos() {
        try {
            this.mostrarLoading(true);
            
            const response = await fetch('/api/produtos/');
            if (response.ok) {
                this.produtos = await response.json();
                this.produtosFiltrados = [...this.produtos];
                this.renderizarTabela();
                this.atualizarEstatisticas();
            } else {
                this.mostrarErro('Erro ao carregar produtos');
            }
        } catch (error) {
            console.error('Erro ao carregar produtos:', error);
            this.mostrarErro('Erro ao conectar com o servidor');
        } finally {
            this.mostrarLoading(false);
        }
    }

    renderizarTabela() {
        const tbody = document.getElementById('corpo-tabela-estoque');
        
        if (this.produtosFiltrados.length === 0) {
            document.getElementById('sem-produtos').style.display = 'block';
            tbody.innerHTML = '';
            return;
        }

        document.getElementById('sem-produtos').style.display = 'none';
        
        tbody.innerHTML = this.produtosFiltrados.map(produto => `
            <tr>
                <td><strong>${produto.id}</strong></td>
                <td>${produto.nome}</td>
                <td>${produto.codigo_barras || 'N/A'}</td>
                <td>${produto.marca || 'N/A'}</td>
                <td>${produto.lote || 'N/A'}</td>
                <td>${this.formatarData(produto.data_validade)}</td>
                <td>R$ ${this.formatarMoeda(produto.preco_custo || 0)}</td>
                <td>R$ ${this.formatarMoeda(produto.preco || produto.preco_venda || 0)}</td>
                <td>${this.renderizarStatus(produto)}</td>
                <td>
                    <button class="btn btn-sm btn-outline-primary btn-action" 
                            onclick="estoqueManager.editarProduto(${produto.id})" 
                            title="Editar">
                        <i class="bi bi-pencil"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-info btn-action" 
                            onclick="estoqueManager.verDetalhes(${produto.id})" 
                            title="Detalhes">
                        <i class="bi bi-eye"></i>
                    </button>
                    <button class="btn btn-sm btn-outline-danger btn-action" 
                            onclick="estoqueManager.excluirProduto(${produto.id})" 
                            title="Excluir">
                        <i class="bi bi-trash"></i>
                    </button>
                </td>
            </tr>
        `).join('');
    }

    renderizarStatus(produto) {
        // Simular status baseado em dados disponíveis
        const hoje = new Date();
        const validade = produto.data_validade ? new Date(produto.data_validade) : null;
        
        if (validade && validade < hoje) {
            return '<span class="status-badge status-vencido">Vencido</span>';
        } else if (validade && (validade - hoje) / (1000 * 60 * 60 * 24) <= 30) {
            return '<span class="status-badge status-baixo">Próximo ao Vencimento</span>';
        } else {
            return '<span class="status-badge status-normal">Normal</span>';
        }
    }

    filtrarProdutos() {
        const busca = document.getElementById('busca-produto').value.toLowerCase();
        const status = document.getElementById('filtro-status').value;
        
        this.produtosFiltrados = this.produtos.filter(produto => {
            const matchBusca = produto.nome.toLowerCase().includes(busca) ||
                             (produto.codigo_barras && produto.codigo_barras.toLowerCase().includes(busca)) ||
                             (produto.marca && produto.marca.toLowerCase().includes(busca));
            
            let matchStatus = true;
            if (status) {
                const hoje = new Date();
                const validade = produto.data_validade ? new Date(produto.data_validade) : null;
                
                switch (status) {
                    case 'vencido':
                        matchStatus = validade && validade < hoje;
                        break;
                    case 'baixo':
                        matchStatus = validade && (validade - hoje) / (1000 * 60 * 60 * 24) <= 30 && validade >= hoje;
                        break;
                    case 'normal':
                        matchStatus = !validade || (validade - hoje) / (1000 * 60 * 60 * 24) > 30;
                        break;
                }
            }
            
            return matchBusca && matchStatus;
        });
        
        this.renderizarTabela();
        this.atualizarEstatisticas();
    }

    ordenarProdutos() {
        const criterio = document.getElementById('ordenar-por').value;
        
        this.produtosFiltrados.sort((a, b) => {
            switch (criterio) {
                case 'nome':
                    return a.nome.localeCompare(b.nome);
                case 'preco':
                    return (a.preco || a.preco_venda || 0) - (b.preco || b.preco_venda || 0);
                case 'validade':
                    const dataA = a.data_validade ? new Date(a.data_validade) : new Date('9999-12-31');
                    const dataB = b.data_validade ? new Date(b.data_validade) : new Date('9999-12-31');
                    return dataA - dataB;
                default:
                    return 0;
            }
        });
        
        this.renderizarTabela();
    }

    atualizarEstatisticas() {
        const total = this.produtosFiltrados.length;
        const hoje = new Date();
        
        let vencidos = 0;
        let proximosVencimento = 0;
        let valorTotal = 0;
        
        this.produtosFiltrados.forEach(produto => {
            const validade = produto.data_validade ? new Date(produto.data_validade) : null;
            const preco = produto.preco_custo || 0;
            
            valorTotal += preco;
            
            if (validade) {
                if (validade < hoje) {
                    vencidos++;
                } else if ((validade - hoje) / (1000 * 60 * 60 * 24) <= 30) {
                    proximosVencimento++;
                }
            }
        });
        
        document.getElementById('total-produtos').textContent = total;
        document.getElementById('produtos-vencidos').textContent = vencidos;
        document.getElementById('proximos-vencimento').textContent = proximosVencimento;
        document.getElementById('valor-total').textContent = `R$ ${this.formatarMoeda(valorTotal)}`;
    }

    limparFiltros() {
        document.getElementById('busca-produto').value = '';
        document.getElementById('filtro-status').value = '';
        document.getElementById('ordenar-por').value = 'nome';
        this.produtosFiltrados = [...this.produtos];
        this.renderizarTabela();
        this.atualizarEstatisticas();
    }

    mostrarLoading(mostrar) {
        document.getElementById('loading').style.display = mostrar ? 'block' : 'none';
    }

    mostrarErro(mensagem) {
        // Implementar notificação de erro
        console.error(mensagem);
        alert(mensagem); // Temporário
    }

    formatarMoeda(valor) {
        return parseFloat(valor).toFixed(2).replace('.', ',');
    }

    formatarData(data) {
        if (!data) return 'N/A';
        return new Date(data).toLocaleDateString('pt-BR');
    }

    // Métodos de ação (placeholder)
    editarProduto(id) {
        alert(`Editar produto ID: ${id} (funcionalidade em desenvolvimento)`);
    }

    verDetalhes(id) {
        const produto = this.produtos.find(p => p.id === id);
        if (produto) {
            alert(`Detalhes do produto:\n\nID: ${produto.id}\nNome: ${produto.nome}\nPreço: R$ ${this.formatarMoeda(produto.preco || produto.preco_venda || 0)}`);
        }
    }

    excluirProduto(id) {
        if (confirm('Tem certeza que deseja excluir este produto?')) {
            alert(`Excluir produto ID: ${id} (funcionalidade em desenvolvimento)`);
        }
    }

    gerarRelatorio() {
        alert('Gerar relatório (funcionalidade em desenvolvimento)');
    }

    atualizarEstoque() {
        this.carregarProdutos();
    }
}

// Funções globais para serem chamadas pelos botões
function limparFiltros() {
    if (window.estoqueManager) {
        window.estoqueManager.limparFiltros();
    }
}

function gerarRelatorio() {
    if (window.estoqueManager) {
        window.estoqueManager.gerarRelatorio();
    }
}

function atualizarEstoque() {
    if (window.estoqueManager) {
        window.estoqueManager.atualizarEstoque();
    }
}

// Inicializar quando o DOM estiver pronto
document.addEventListener('DOMContentLoaded', function() {
    window.estoqueManager = new EstoqueManager();
});
