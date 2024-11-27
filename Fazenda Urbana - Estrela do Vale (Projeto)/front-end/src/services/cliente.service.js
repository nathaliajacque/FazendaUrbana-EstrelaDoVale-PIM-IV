const api = require('./api');

async function listarClientes() {
    try {
        const response = await api.get('/clientes/');
        return response.data;
    } catch (error) {
        console.error('Erro ao buscar todos os Clientes:', error.response?.data || error.message);
        throw error;
    }
}

async function buscarClientePorId(id) {
    try {
        const response = await api.get(`/clientes/${id}/`);
        return response.data;
    } catch (error) {
        console.error('Erro ao buscar Cliente:', error.response?.data || error.message);
        throw error;
    }
}

async function criarCliente(data) {
    try {
        const response = await api.post('/clientes/criar/', data);
        return response.data;
    } catch (error) {
        console.error('Erro ao criar Clientes:', error.response?.data || error.message);
        throw error;
    }
}

async function editarCliente(id, data) {
    try {
        const response = await api.put(`/clientes/editar/${id}/`, data);
        return response.data;
    } catch (error) {
        console.error('Erro ao editar Clientes:', error.response?.data || error.message);
        throw error;
    }
}

module.exports = {
    listarClientes,
    buscarClientePorId,
    criarCliente,
    editarCliente
};