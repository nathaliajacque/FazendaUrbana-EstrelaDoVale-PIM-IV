// services/userService.js
const api = require('./api');

async function listarUsuarios() {
    try {
        const response = await api.get('/usuarios/');
        return response.data;
    } catch (error) {
        console.error('Erro ao buscar usuários:', error.response?.data || error.message);
        throw error;
    }
}

async function buscarUsuarioPorId(id) {
    try {
        const response = await api.get(`/usuarios/${id}/`, );
        return response.data;
    } catch (error) {
        console.error('Erro ao buscar usuário:', error.response?.data || error.message);
        throw error;
    }
}

async function criarUsuario(email, password, outrosDados) {
    try {
        const response = await api.post('/usuarios/criar/', {
            email,
            password,
            ...outrosDados,
        });
        return response.data;
    } catch (error) {
        console.error('Erro ao criar usuário:', error.response?.data || error.message);
        throw error;
    }
}
async function editarUsuario(id, dadosAtualizados) {
    try {
        const response = await api.put(`/usuarios/editar/${id}/`, dadosAtualizados);
        return response.data;
    } catch (error) {
        console.error('Erro ao editar usuário:', error.response?.data || error.message);
        throw error;
    }
}
async function loginUsuario(email, password) {
    try {
        const response = await api.post('/login/', { email, password });
        return response.data;
    } catch (error) {
        console.error('Erro ao fazer login:', error.response?.data || error.message);
        throw error;
    }
}
async function logoutUsuario() {
    try {
        const response = await api.post('/logout/');
        return response.data;
    } catch (error) {
        console.error('Erro ao fazer logout:', error.response?.data || error.message);
        throw error;
    }
}

module.exports = {listarUsuarios,buscarUsuarioPorId, criarUsuario, editarUsuario, loginUsuario, logoutUsuario };
