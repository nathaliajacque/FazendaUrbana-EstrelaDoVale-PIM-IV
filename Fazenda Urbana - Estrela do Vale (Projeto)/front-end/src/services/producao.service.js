const api = require('./api');

async function listarProducoes() {
    try {
        const response = await api.get('/producoes/');
        return response.data;
    } catch (error) {
        console.error('Erro ao buscar todos os Produçoes:', error.response?.data || error.message);
        throw error;
    }
}

async function buscarProducaoPorId(id) {
    try {
        const response = await api.get(`/producoes/${id}/`);
        return response.data;
    } catch (error) {
        console.error('Erro ao buscar Producao:', error.response?.data || error.message);
        throw error;
    }
}

async function criarProducao(data) {
    try {
        const response = await api.post('/producoes/criar/', data);
        return response.data;
    } catch (error) {
        console.error('Erro ao criar Producoes:', error.response?.data || error.message);
        throw error;
    }
}

async function editarProducao(id, data) {
    try {
        const response = await api.put(`/producoes/editar/${id}/`, data);
        return response.data;
    } catch (error) {
        console.error('Erro ao editar Producoes:', error.response?.data || error.message);
        throw error;
    }
}

module.exports = {
    listarProducoes,
    buscarProducaoPorId,
    criarProducao,
    editarProducao
};