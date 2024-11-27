// services/funcionarioService.js
const api = require('./api');

async function listarFuncionarios() {
    try {
        const response = await api.get('/funcionarios/');
        return response.data;
    } catch (error) {
        console.error('Erro ao buscar funcionários:', error.response?.data || error.message);
        throw error;
    }
}

async function buscarFuncionarioPorId(id) {
    try {
        const response = await api.get(`/funcionarios/${id}/`);
        return response.data;
    } catch (error) {
        console.error('Erro ao buscar funcionário:', error.response?.data || error.message);
        throw error;
    }
}

async function criarFuncionario(data) {
    try {
        const response = await api.post('/funcionarios/criar/', data);
        return response.data;
    } catch (error) {
        console.error('Erro ao criar funcionário:', error.response?.data || error.message);
        throw error;
    }
}

async function editarFuncionario(id, data) {
    try {
        const response = await api.put(`/funcionarios/editar/${id}/`, data);
        return response.data;
    } catch (error) {
        console.error('Erro ao editar funcionário:', error.response?.data || error.message);
        throw error;
    }
}

module.exports = {
    listarFuncionarios,
    buscarFuncionarioPorId,
    criarFuncionario,
    editarFuncionario
};
