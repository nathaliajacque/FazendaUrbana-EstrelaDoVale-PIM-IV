const userService = require('../../../services/user.service');
const { listarFuncionarios } = require('../../../services/funcionario.service');
const {listarFornecedores} = require('../../../services/fornecedor.service');
const {listarClientes} = require('../../../services/cliente.service');
const {listarProdutos} = require('../../../services/produto.service');
const {listarPedidos} = require('../../../services/pedido.service');

document.addEventListener('DOMContentLoaded', async () => {
    try {
        const funcionarios = await listarFuncionarios();
        const fornecedores = await listarFornecedores();
        const clientes = await listarClientes();
        const produtos = await listarProdutos();
        const pedidos = await listarPedidos();
        const usuarios = await userService.listarUsuarios();
        const divUsuarios = document.querySelector('.div1');
        const divFuncionarios = document.querySelector('.div2');
        const divFornecedores = document.querySelector('.div4');
        const divClientes = document.querySelector('.div');
        const divProdutos = document.querySelector('.div5');
        const divPedidos = document.querySelector('.div3');
        const nomeUser = document.querySelector('#nomeUser');
        divUsuarios.textContent = usuarios.length;
        divFuncionarios.textContent = funcionarios.length;
        divFornecedores.textContent = fornecedores.length;
        divClientes.textContent = clientes.length;
        divProdutos.textContent = produtos.length;
        divPedidos.textContent = pedidos.length;
        nomeUser.textContent=localStorage.getItem('name');
        const buttonProd = document.querySelector('#producao');
        buttonProd.addEventListener('click', async (event)=>{
            event.preventDefault();
            window.location.href = '../PesquisaProducao/PesquisaProducao.html';
        });
    } catch (error) {
        console.error('Erro ao buscar a lista de usuários:', error);
    }
});
