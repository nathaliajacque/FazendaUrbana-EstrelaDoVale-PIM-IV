const api = require('./api');

async function listarPedidos() {
    try {
        const response = await api.get('/pedidos/');
        return response.data;
    } catch (error) {
        console.error('Erro ao buscar todos os Pedidos:', error.response?.data || error.message);
        throw error;
    }
}

async function buscarPedidoPorId(id) {
    try {
        const response = await api.get(`/pedidos/${id}/`);
        return response.data;
    } catch (error) {
        console.error('Erro ao buscar Pedido:', error.response?.data || error.message);
        throw error;
    }
}

async function criarPedido(data) {
    try {
        const response = await api.post('/pedidos/criar/', data);
        return response.data;
    } catch (error) {
        console.error('Erro ao criar Pedidos:', error.response?.data || error.message);
        throw error;
    }
}

async function editarPedido(id, data) {
    try {
        const response = await api.put(`/pedidos/editar/${id}/`, data);
        return response.data;
    } catch (error) {
        console.error('Erro ao editar Pedidos:', error.response?.data || error.message);
        throw error;
    }
}

module.exports = {
    listarPedidos,
    buscarPedidoPorId,
    criarPedido,
    editarPedido
};