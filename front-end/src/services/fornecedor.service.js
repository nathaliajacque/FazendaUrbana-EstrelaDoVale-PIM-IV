const api = require('./api');

async function listarFornecedores() {
    try {
        const response = await api.get('/fornecedores/');
        return response.data;
    } catch (error) {
        console.error('Erro ao buscar fornecedores:', error.response?.data || error.message);
        throw error;
    }
}

async function buscarFornecedorPorId(id) {
    try {
        const response = await api.get(`/fornecedores/${id}/`);
        return response.data;
    } catch (error) {
        console.error('Erro ao buscar fornecedor:', error.response?.data || error.message);
        throw error;
    }
}

async function criarFornecedor(data) {
    try {
        const response = await api.post('/fornecedores/criar/', data);
        return response.data;
    } catch (error) {
        console.error('Erro ao criar fornecedor:', error.response?.data || error.message);
        throw error;
    }
}

async function editarFornecedor(id, data) {
    try {
        const response = await api.put(`/fornecedores/editar/${id}/`, data);
        return response.data;
    } catch (error) {
        console.error('Erro ao editar funcionário:', error.response?.data || error.message);
        throw error;
    }
}

module.exports = {
    listarFornecedores,
    buscarFornecedorPorId,
    criarFornecedor,
    editarFornecedor
};
