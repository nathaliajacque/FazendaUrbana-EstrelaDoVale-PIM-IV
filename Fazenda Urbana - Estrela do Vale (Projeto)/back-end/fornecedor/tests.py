from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import (
    Fornecedor,
    Usuario,
)
import json

Usuario = get_user_model()


class FornecedorAPITests(TestCase):
    def setUp(self):
        self.client = Client()

        # Criar um usuário de teste
        self.user = Usuario.objects.create_user(
            email="testuser@example.com", password="testpassword", nivel_acesso="ADMINISTRADOR"
        )

        # Obter JWT token para o usuario de teste
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        # Autenticar o usuário de teste
        self.client.login(email="testuser@example.com", password="testpassword")

        self.fornecedor_data = {
            "nome_fantasia": "Fornecedor Teste",
            "razao_social": "Fornecedor Teste LTDA",
            "cnpj": "12345678000195",  # Um CNPJ fictício válido
            "ie": "1234567890",
            "im": "1234567890",
            "contato": "Contato Teste",
            "email": "contato@test.com",
            "logradouro": "Rua Teste",
            "bairro": "Bairro Teste",
            "numero": "123",
            "cep": "12345-678",
            "complemento": "Apto 1",
            "cidade": "Cidade Teste",
            "uf": "SP",
            "observacao": "Observação teste",
            "prazo_entrega_dias": 5,
            "usuario": self.user,  # Associar o fornecedor ao usuário de teste
        }
        self.fornecedor = Fornecedor.objects.create(**self.fornecedor_data)


    def test_get_lista(self):
        response = self.client.get(
            reverse("fornecedor:get_lista"),
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.fornecedor.nome_fantasia)

    def test_get_detalhe(self):
        response = self.client.get(
            reverse("fornecedor:get_detalhe", args=[self.fornecedor.id]),
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertEqual(
            response.json()["nome_fantasia"], self.fornecedor_data["nome_fantasia"]
        )

    def test_post_criar(self):
        self.fornecedor_data["cnpj"] = "59598388000117"
        self.fornecedor_data["usuario"] = self.user.id

        response = self.client.post(
            reverse("fornecedor:post_criar"),
            data=json.dumps(self.fornecedor_data),
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )

        print(response.content)
        self.assertEqual(response.status_code, 201)
        self.assertIn("id", response.json())

    def test_put_editar(self):
        updated_data = {"nome_fantasia": "Fornecedor Atualizado"}
        response = self.client.put(
            reverse("fornecedor:put_editar", args=[self.fornecedor.pk]),
            data=json.dumps(updated_data),
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        self.assertEqual(response.status_code, 200)
        self.fornecedor.refresh_from_db()
        self.assertEqual(self.fornecedor.nome_fantasia, "Fornecedor Atualizado")

    def test_get_detalhe_not_found(self):
        response = self.client.get(
            reverse("fornecedor:get_detalhe", args=[999]),  # ID que não existe
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        self.assertEqual(response.status_code, 404)

    def test_put_editar_not_found(self):
        updated_data = {"nome_fantasia": "Fornecedor Atualizado"}
        response = self.client.put(
            reverse("fornecedor:put_editar", args=[999]),
            data=json.dumps(updated_data),
            content_type="application/json",
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        self.assertEqual(response.status_code, 404)