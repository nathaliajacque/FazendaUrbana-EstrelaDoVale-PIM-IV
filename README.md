# Fazenda Urbana - Estrela do Vale - PIM IV
Este é um projeto para gerenciar uma fazenda urbana chamada Estrela do Vale, desenvolvido como parte do PIM IV. O backend foi implementado em Python utilizando o framework Django, com o banco de dados SQL Server hospedado em um container Docker para garantir independência e facilitar a implantação em diferentes ambientes. O front-end foi desenvolvido em JavaScript utilizando o Electron, proporcionando uma interface desktop amigável e funcional. O sistema, desenvolvido pela empresa SAPOO :frog:, permite o gerenciamento de usuários, clientes, funcionários, fornecedores, produtos, pedidos e produções, facilitando a administração das operações da fazenda.

## 📫 Diagramas UML desenvolvido para a Fazenda Urbana Estrela do Vale :frog:

Os diagramas UML (Unified Modeling Language) são fundamentais em projetos de desenvolvimento de software, pois facilitam a compreensão, promovem a clareza, reduzem riscos de comunicação, melhoram o planejamento, suportam a implementação e facilitam a manutenção do sistema. Eles ajudam a construir um entendimento comum entre a equipe e garantem que o sistema seja desenvolvido de maneira organizada e alinhada com os requisitos e expectativas do cliente.

1. Diagrama de Caso de Uso e de Classe de Implementação: [Clique aqui para acessar](https://github.com/nathaliajacque/Fazenda---PIM-IV/tree/Fazenda_PIMIV/Fazenda%20Urbana%20-%20Estrela%20do%20Vale%20(Diagramas%20UML)/Diagrama%20de%20Caso%20de%20Uso).
2. Diagrama de Classe: [Clique aqui para acessar](https://github.com/nathaliajacque/Fazenda---PIM-IV/tree/Fazenda_PIMIV/Fazenda%20Urbana%20-%20Estrela%20do%20Vale%20(Diagramas%20UML)/Diagrama%20de%20Classe).
3. Diagrama de Sequencia: [Clique aqui para acessar](https://github.com/nathaliajacque/Fazenda---PIM-IV/tree/Fazenda_PIMIV/Fazenda%20Urbana%20-%20Estrela%20do%20Vale%20(Diagramas%20UML)/Diagrama%20de%20Sequ%C3%AAncia).
4. Diagrama de Atividade: [Clique aqui para acessar](https://github.com/nathaliajacque/Fazenda---PIM-IV/tree/Fazenda_PIMIV/Fazenda%20Urbana%20-%20Estrela%20do%20Vale%20(Diagramas%20UML)/Diagrama%20de%20Atividade%20-%20Collection).
5. Diagrama de Implantação: [Clique aqui para acessar](https://github.com/nathaliajacque/Fazenda---PIM-IV/tree/Fazenda_PIMIV/Fazenda%20Urbana%20-%20Estrela%20do%20Vale%20(Diagramas%20UML)/Diagrama%20de%20Implanta%C3%A7%C3%A3o).


Como alternativa, baixe a documentação de todos os diagramas acima no formato .ASTAH [Clique aqui para acessar](https://github.com/nathaliajacque/Fazenda---PIM-IV/blob/Fazenda_PIMIV/Fazenda%20Urbana%20-%20Estrela%20do%20Vale%20(Diagramas%20UML)/Fazenda%20Urbana%20-%20EstrelaDoVale.asta).



## Requisitos - (Back-end)

- **Python 3.x**
- **Django**
- **pyodbc**
- **SQL Server**
- **Outras dependências estão dentro de `requirements.txt`**

## Requisitos - (Front-end)

- **Node.js**
- **npm** ou **yarn**
- **Outras dependências estão dentro de `package.json`**


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

   Para o back-end:
   ```sh
   pip install -r requirements.txt
   ```

   Para o front-end:
   ```sh
   npm install
   # ou
   yarn install
   ```

4. Inicie o servidor de desenvolvimento:

   ```sh
   python manage.py runserver
   ```

## Docker
O projeto está configurado para ser executado em contêineres Docker. Isso garante um ambiente de desenvolvimento consistente e facilita a implantação.

1. Construir a Imagem Docker:

   ```sh
   docker-compose build
   ```

2. Iniciar os Contêineres:

   ```sh
   docker-compose up
   ```


## Uso
Acesse o servidor de desenvolvimento em `http://127.0.0.1:8000/`.
Use as URLs configuradas no arquivo `urls.py` para acessar as diferentes funcionalidades do projeto.
Para o front-end utilize `http://localhost:3000.`


## Estrutura do Projeto - Back-end

### Diretório Principal do Projeto (estreladovale):
- `settings.py`: Configurações globais do projeto Django.
- `urls.py`: Configurações de roteamento globais do projeto.
 

### Cada diretório de aplicação contém os seguintes arquivos principais:
- `apps.py`: Configurações da aplicação.
- `models.py`: Definições dos modelos de dados.
- `serializers.py`: Serializadores para transformar os dados dos modelos em JSON e vice-versa.
- `tests.py`: Testes automatizados para a aplicação.
- `urls.py`: Configurações de roteamento específicas da aplicação.
- `views.py`: Lógica das views da aplicação.
- `migrations/`: Diretório que contém as migrações do banco de dados para a aplicação.
 

## Estrutura do Projeto - Front-end
- `src/`: Contém o código-fonte do projeto.
  - `components/`: Componentes reutilizáveis da interface do usuário.
  - `pages/`: Páginas principais da aplicação.
  - `services/`: Serviços para comunicação com a API back-end.
  - `styles/`: Arquivos de estilo CSS.
  - `App.js`: Componente principal da aplicação.
  - `index.js`: Ponto de entrada da aplicação.


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

## Testes
Os testes estão localizados no arquivo tests.py dentro de fornecedor/tests.py e funcionario/tests.py. Eles verificam a funcionalidade da API para garantir que as operações CRUD funcionem conforme esperado.

   ```sh
   pytest
   ```

:frog:
