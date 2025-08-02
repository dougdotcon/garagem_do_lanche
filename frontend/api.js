/**
 * Cliente JavaScript para comunicação com a API da Garagem do Lanche
 */

const API_BASE_URL = 'http://localhost:5000/api';

class GaragemAPI {
    constructor() {
        this.baseURL = API_BASE_URL;
    }

    /**
     * Faz uma requisição HTTP para a API
     */
    async request(endpoint, options = {}) {
        const url = `${this.baseURL}${endpoint}`;
        const config = {
            headers: {
                'Content-Type': 'application/json',
                ...options.headers
            },
            credentials: 'include', // Para incluir cookies de sessão
            ...options
        };

        try {
            const response = await fetch(url, config);
            const data = await response.json();
            
            if (!response.ok) {
                throw new Error(data.error || `HTTP ${response.status}`);
            }
            
            return data;
        } catch (error) {
            console.error(`Erro na requisição para ${endpoint}:`, error);
            throw error;
        }
    }

    // === CARDÁPIO ===
    async getCardapio() {
        return this.request('/cardapio');
    }

    async getPrato(id) {
        return this.request(`/cardapio/${id}`);
    }

    async getAcompanhamentos() {
        return this.request('/acompanhamentos');
    }

    // === PEDIDOS ===
    async criarPedido(dadosPedido) {
        return this.request('/pedidos', {
            method: 'POST',
            body: JSON.stringify(dadosPedido)
        });
    }

    async listarPedidos(filtros = {}) {
        const params = new URLSearchParams(filtros);
        const endpoint = `/pedidos${params.toString() ? '?' + params.toString() : ''}`;
        return this.request(endpoint);
    }

    async getPedido(id) {
        return this.request(`/pedidos/${id}`);
    }

    async atualizarStatusPedido(id, status) {
        return this.request(`/pedidos/${id}/status`, {
            method: 'PUT',
            body: JSON.stringify({ status })
        });
    }

    async getPedidosCozinha() {
        return this.request('/pedidos/cozinha');
    }

    // === CAIXA ===
    async getRelatorioCaixa(dataInicio = null, dataFim = null) {
        const params = new URLSearchParams();
        if (dataInicio) params.append('data_inicio', dataInicio);
        if (dataFim) params.append('data_fim', dataFim);
        
        const endpoint = `/caixa/relatorio${params.toString() ? '?' + params.toString() : ''}`;
        return this.request(endpoint);
    }

    async getDashboardCaixa() {
        return this.request('/caixa/dashboard');
    }

    async criarMovimentacao(dadosMovimentacao) {
        return this.request('/caixa/movimentacao', {
            method: 'POST',
            body: JSON.stringify(dadosMovimentacao)
        });
    }

    // === AUTENTICAÇÃO ===
    async login(senha) {
        return this.request('/auth/login', {
            method: 'POST',
            body: JSON.stringify({ senha })
        });
    }

    async logout() {
        return this.request('/auth/logout', {
            method: 'POST'
        });
    }

    async checkAuth() {
        return this.request('/auth/check');
    }

    // === UTILITÁRIOS ===
    async healthCheck() {
        return this.request('/health');
    }

    async getApiInfo() {
        return this.request('/info');
    }
}

// Instância global da API
const api = new GaragemAPI();

// Funções auxiliares para compatibilidade com o código existente
async function carregarCardapio() {
    try {
        const response = await api.getCardapio();
        return response.pratos;
    } catch (error) {
        console.error('Erro ao carregar cardápio:', error);
        return [];
    }
}

async function carregarAcompanhamentos() {
    try {
        const response = await api.getAcompanhamentos();
        return response.acompanhamentos;
    } catch (error) {
        console.error('Erro ao carregar acompanhamentos:', error);
        return [];
    }
}

async function enviarPedido(dadosPedido) {
    try {
        const response = await api.criarPedido(dadosPedido);
        return response.pedido;
    } catch (error) {
        console.error('Erro ao enviar pedido:', error);
        throw error;
    }
}

async function verificarStatusPedido(pedidoId) {
    try {
        const response = await api.getPedido(pedidoId);
        return response.pedido;
    } catch (error) {
        console.error('Erro ao verificar status do pedido:', error);
        return null;
    }
}

// Função para calcular taxa de entrega (mantém compatibilidade)
function calcularTaxaEntrega(bairro) {
    if (!bairro) return 5.00;
    const nome = bairro.toLowerCase();
    if (nome.includes("gramacho")) return 1.00;
    if (nome.includes("centro")) return 2.00;
    if (nome.includes("parque") || nome.includes("vila")) return 3.00;
    if (nome.includes("jardim") || nome.includes("mutuá")) return 4.00;
    return 5.00;
}

// Exportar para uso em módulos
if (typeof module !== 'undefined' && module.exports) {
    module.exports = { GaragemAPI, api };
}
