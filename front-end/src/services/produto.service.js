
const api = require('./api');

async function listarProdutos() {
    try {
        const response = await api.get('/produtos/');
        return response.data;
    } catch (error) {
        console.error('Erro ao buscar Produtos:', error.response?.data || error.message);
        throw error;
    }
}

async function buscarProdutoPorId(id) {
    try {
        const response = await api.get(`/produtos/${id}/`);
        return response.data;
    } catch (error) {
        console.error('Erro ao buscar Produto:', error.response?.data || error.message);
        throw error;
    }
}

async function criarProduto(data) {
    try {
        const response = await api.post('/produtos/criar/', data);
        return response.data;
    } catch (error) {
        console.error('Erro ao criar Produto:', error.response?.data || error.message);
        throw error;
    }
}

async function editarProduto(id, data) {
    try {
        const response = await api.put(`/produtos/editar/${id}/`, data);
        return response.data;
    } catch (error) {
        console.error('Erro ao editar Produto:', error.response?.data || error.message);
        throw error;
    }
}

module.exports = {
    listarProdutos,
    buscarProdutoPorId,
    criarProduto,
    editarProduto
};
