const axios = require('axios');

const api = axios.create({
    baseURL: 'http://127.0.0.1:8000/', // Substitua pela URL do backend
    headers: {
        'Content-Type': 'application/json',
    },
    withCredentials: true, // Inclui cookies para sessões (caso necessário)
    //timeout: 10000
});

api.interceptors.request.use(config => {
    const token = localStorage.getItem('authToken');
    if (token) {
        config.headers.Authorization = `Bearer ${token}`;
    }
    return config;
}, error => {
    return Promise.reject(error);
});

module.exports = api;
