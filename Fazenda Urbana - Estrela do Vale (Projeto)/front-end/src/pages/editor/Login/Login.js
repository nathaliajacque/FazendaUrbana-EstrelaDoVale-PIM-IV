const userService = require('../../../services/user.service');

document.addEventListener('DOMContentLoaded', () => {
    const form = document.querySelector('form');
    const loginButton = document.querySelector('#entrar');
    form.addEventListener('submit', async (event) => {
        event.preventDefault();

        const email = document.querySelector('#email').value;
        const password = document.querySelector('#senha').value;
        try {
            const response = await userService.loginUsuario(email, password);

            if (response.message === 'Login realizado com sucesso') {
                
                localStorage.setItem('authToken', response.access);
                localStorage.setItem('name', response.name);
                loginButton.disabled = false;
                window.location.href = '../Dashboard/Dashboard.html';
            } else {
                alert('Credenciais inválidas');
            }
        } catch (error) {
            console.error('Erro ao fazer login:', error);
            alert('Erro ao conectar ao servidor');            
        }
    });
});
