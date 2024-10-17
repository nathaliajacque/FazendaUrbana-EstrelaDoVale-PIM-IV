# Documentação da API de Fornecedores

A API para gerenciar fornecedores está hospedada em `http://localhost:8000/fornecedor/`. Esta API permite realizar operações de CRUD (Criar, Ler, Atualizar, Deletar) sobre o modelo `Fornecedor`.

## 1. Listar Fornecedores

**Método:** `GET`  
**URL:** `/fornecedor/`

### Descrição:
Retorna uma lista de todos os fornecedores cadastrados.

### Resposta:
- **Código 200 (OK)**: Retorna um JSON com a lista de fornecedores.
- **Exemplo de Resposta:**
    ```json
    [
        {
            "id": 1,
            "nome_fantasia": "Fornecedor Teste",
            "razao_social": "Fornecedor Teste LTDA",
            ...
        },
        ...
    ]
    ```

---

## 2. Detalhe do Fornecedor

**Método:** `GET`  
**URL:** `/fornecedor/<id>/` (substitua `<id>` pelo ID do fornecedor)

### Descrição:
Retorna os detalhes de um fornecedor específico.

### Resposta:
- **Código 200 (OK)**: Retorna um JSON com os detalhes do fornecedor.
- **Código 404 (Não Encontrado)**: Se o fornecedor não existir.
- **Exemplo de Resposta:**
    ```json
    {
        "id": 1,
        "nome_fantasia": "Fornecedor Teste",
        "razao_social": "Fornecedor Teste LTDA",
        ...
    }
    ```

---

## 3. Criar Fornecedor

**Método:** `POST`  
**URL:** `/fornecedor/criar/`

### Descrição:
Cria um novo fornecedor.

### Requisição:
Envie um JSON no corpo da requisição com os seguintes campos:
```json
{
    "nome_fantasia": "Fornecedor Teste",
    "razao_social": "Fornecedor Teste LTDA",
    "cnpj": "12345678000195",
    "ie": "1234567890",
    "im": "1234567890",
    "contato": "Contato Teste",
    "email_1": "contato@test.com",
    "email_2": "contato2@test.com",
    "logradouro": "Rua Teste",
    "bairro": "Bairro Teste",
    "numero": "123",
    "cep": "12345-678",
    "complemento": "Apto 1",
    "cidade": "Cidade Teste",
    "uf": "SP",
    "observacao": "Observação teste",
    "prazo_entrega_dias": 5
}
```
### Resposta:
- **Código 201 (Criado)**: Retorna o ID do novo fornecedor.
- **Código 400 (Bad Request)** Se os dados enviados estiverem inválidos.
- **Exemplo de Resposta:**
```json
{
    "id": 1
}
```
## 4. Editar Fornecedor

**Método:** `PUT`  
**URL:** `/fornecedor/editar/<id>/` (substitua `<id>` pelo ID do fornecedor)

### Descrição:
Atualiza os dados de um fornecedor existente.

### Requisição:
Envie um JSON no corpo da requisição com os campos que deseja atualizar. Somente os campos enviados serão alterados:
```json
{
    "nome_fantasia": "Novo Nome Fantasia",
    "razao_social": "Nova Razão Social"
}
```

### Respostas:
- **Código 200 (OK):** Atualização bem-sucedida. Retorna o ID do fornecedor atualizado.  
  **Exemplo de Resposta:**
```json
  {
      "id": 1
  }
        ```

- **Código 400 (Bad Request):** O corpo da requisição está inválido ou contém dados não válidos.  
  **Exemplos de Resposta:**
```json
  {
      "erro": "Corpo da requisição inválido"
  }
              ```
```json
  {
      "erro": {
          "nome_fantasia": ["Este campo é obrigatório."]
      }
  }
```
- **Código 404 (Not Found):** Fornecedor não encontrado para o ID fornecido.  
  **Exemplo de Resposta:**
```json
  {
      "erro": "Fornecedor não encontrado"
  }
```
- **Código 405 (Method Not Allowed):** Método HTTP não permitido. Esta rota aceita apenas `PUT`.  
  **Exemplo de Resposta:**
```json
  {
      "erro": "Método não permitido"
  }
```
- **Código 500 (Internal Server Error):** Erro inesperado no servidor.  
  **Exemplo de Resposta:**
```json
  {
      "erro": "Erro inesperado <detalhes do erro>"
  }
```