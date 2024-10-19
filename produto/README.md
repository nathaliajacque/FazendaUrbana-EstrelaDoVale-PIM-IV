# Documentação da API de Produtos

A API para gerenciar produtos está hospedada em `http://localhost:8000/produtos/`. Esta API permite realizar operações de CRUD (Criar, Ler e Atualizar) sobre o modelo `Produto`.

## 1. Listar Produtos

**Método:** `GET`  
**URL:** `/produtos/`

### Descrição:
Retorna uma lista de todos os produtos cadastrados.

### Resposta:
- **Código 200 (OK)**: Retorna um JSON com a lista de produtos.
- **Exemplo de Resposta:**
```json
[
    {
        "id": 1,
        "descricao": "Produto Teste",
        "categoria": "Categoria Teste",
        "fornecedor": 1,
        "grupo": "Grupo Teste",
        "temperatura": 25.0,
        "umidade": 60.0,
        "iluminacao": 1000.0,
        "crescimento": 30,
        "intensidade_led": 500.0,
        "nivel_agua": 10.0,
        "solucao_nutritiva": "Solução Teste",
        "observacao": "Observação Teste",
        "status": "Ativo",
        "data_cadastro": "2024-10-19T01:01:56Z"
    },
    ...
]
```

---

## 2. Detalhe do Produto

**Método**: `GET`
**URL**: `/produtos/<id>/` (substitua `<id>` pelo ID do produto)

### Descrição:
Retorna os detalhes de um produto específico.

### Resposta:
- **Código 200 (OK)**: Retorna um JSON com os detalhes do produto.
- **Código 404 (Não Encontrado)**: Se o produto não existir.
 **Exemplo de Resposta:**
```json
{
    "id": 1,
    "descricao": "Produto Teste",
    "categoria": "TUBERCULO",
    "fornecedor": 1,
    "grupo": "Grupo Teste",
    "temperatura": 25.0,
    "umidade": 60.0,
    "iluminacao": 1000.0,
    "crescimento": 30,
    "intensidade_led": 500.0,
    "nivel_agua": 10.0,
    "solucao_nutritiva": "Solução Teste",
    "observacao": "Observação Teste",
    "status": "Ativo",
    "data_cadastro": "2024-10-19T01:01:56Z"
}
```

---

## 3. Criar Produto
**Método:** `POST`
**URL:** `/produtos/criar/`

### Descrição:
Cria um novo produto.

### Requisição:
Envie um JSON no corpo da requisição com os seguintes campos:
```json
{
    "descricao": "Produto Teste",
    "categoria": "Categoria Teste",
    "fornecedor": 1,
    "grupo": "Grupo Teste",
    "temperatura": 25.0,
    "umidade": 60.0,
    "iluminacao": 1000.0,
    "crescimento": 30,
    "intensidade_led": 500.0,
    "nivel_agua": 10.0,
    "solucao_nutritiva": "Solução Teste",
    "observacao": "Observação Teste"
}
```
### Resposta:
- **Código 201 (Criado):** Retorna o ID do novo produto.
- **Código 400 (Bad Request):** Se os dados enviados estiverem inválidos.
- **Código 404 (Não Encontrado):** Se o fornecedor não existir.
 **Exemplo de Resposta:**
```json
{
    "id": 1
}
```

---

## 4. Editar Produto
**Método:** PUT
**URL:** `/produtos/editar/<id>/` (substitua `<id>` pelo ID do produto)

### Descrição:
Atualiza os dados de um produto existente.

### Requisição:
Envie um JSON no corpo da requisição com os campos que deseja atualizar. Somente os campos enviados serão alterados:
```json
{
    "descricao": "Novo Produto Teste",
    "categoria": "Nova Categoria Teste"
}
```

### Respostas:
- **Código 200 (OK):** Atualização bem-sucedida. Retorna o ID do produto atualizado.
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
        "descricao": ["Este campo é obrigatório."]
    }
}
```
- **Código 404 (Not Found):** Produto não encontrado para o ID fornecido.
 **Exemplos de Resposta:**
```json
 {
    "erro": "Produto não encontrado"
}
```
- **Código 405 (Method Not Allowed):** Método HTTP não permitido. Esta rota aceita apenas PUT.
 **Exemplos de Resposta:**
```json
{
    "erro": "Método não permitido"
}
```
- **Código 500 (Internal Server Error):** Erro inesperado no servidor.
 **Exemplos de Resposta:**
```json
{
    "erro": "Erro inesperado <detalhes do erro>"
}
```