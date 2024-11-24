# Fazenda Urbana - Estrela do Vale - PIM IV

Este é um projeto Django para gerenciar uma fazenda urbana chamada Estrela do Vale, desenvolvido como parte do PIM IV. O sistema desenvolvido pela empresa SAPOO :frog: permite o gerenciamento de usuários, clientes, funcionários, fornecedores, produtos, pedidos e produções facilitando a administração das operações da fazenda. 


## Requisitos

- **Python 3.x**
- **Django**
- **pyodbc**
- **SQL Server**
- **Outras dependências então dentro de requirements.txt**


## Instalação

1. Clone o repositório:

   ```sh
   git clone https://github.com/nathaliajacque/Fazenda---PIM-IV.git
   cd Fazenda---PIM-IV
   ```

2. Crie e ative um ambiente virtual:

   ```sh
   python -m venv venv
   venv\Scripts\activate  # No Windows
   ```

3. Instale as dependências:

   ```sh
   pip install -r requirements.txt
   ```

4. Inicie o servidor de desenvolvimento:

   ```sh
   python manage.py runserver
   ```


### Uso
Acesse o servidor de desenvolvimento em `http://127.0.0.1:8000/`.
Use as URLs configuradas no arquivo `urls.py` para acessar as diferentes funcionalidades do projeto.


### Estrutura do Projeto
`urls.py:` Configurações de roteamento do projeto.
`views.py:` Lógica das views do projeto.
`models.py:` Definições dos modelos de dados.
`settings.py:` Configurações do projeto.


## Funcionalidades
Abaixo está um exemplo que como utilizar o objeto `Usuário` que segue para todos os outros objetos deste projeto.

### Usuários

- **Listar Usuários**: Retorna uma lista de todos os usuários cadastrados.
  - **URL**: `usuario`


  - **Método HTTP**: `GET`
  - **Resposta**: JSON com a lista de usuários.

- **Detalhar Usuário**: Retorna os detalhes de um usuário específico.
  - **URL**: `/usuario/<int:pk>/`
  - **Método HTTP**: `GET`
  - **Resposta**: JSON com os detalhes do usuário.

- **Criar Usuário**: Cria um novo usuário.
  - **URL**: `/usuario/criar/`
  - **Método HTTP**: `POST`
  - **Resposta**: JSON com o ID do usuário criado.

- **Editar Usuário**: Edita um usuário existente.
  - **URL**: `/usuario/editar/<int:pk>/`
  - **Método HTTP**: `PUT`
  - **Resposta**: JSON com os detalhes do usuário atualizado.