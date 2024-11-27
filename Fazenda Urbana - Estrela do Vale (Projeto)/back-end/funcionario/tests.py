from django.test import TestCase, Client
from django.urls import reverse
from django.contrib.auth import get_user_model
from rest_framework_simplejwt.tokens import RefreshToken
from .models import Funcionario
import json

Usuario = get_user_model()


class FuncionarioAPITests(TestCase):
    def setUp(self):
        self.client = Client()

        # Criar um usuário de teste
        self.user = Usuario.objects.create_user(
            email="testuser@example.com",
            password="testpassword",
            nivel_acesso="ADMINISTRADOR",
        )

        # Autenticar o usuário de teste
        self.client.login(email="testuser@example.com", password="testpassword")


        # Obter JWT token para o usuario de teste
        refresh = RefreshToken.for_user(self.user)
        self.access_token = str(refresh.access_token)

        self.funcionario_data = {
            "nome": "Eduardo Pereira da Silva",
            "cargo": "GERENTE_DE_PRODUCAO_AGRICOLA",
            "cpf": "12345678901",
            "rg": "MG1234567",
            "orgao_emissor": "SSP/MG",
            "contato": "(31) 98765-4321",
            "email": "joao.silva@example.com",
            "data_admissao": "2023-01-15",
            "data_cadastro": "2024-10-20T00:09:27.623837-03:00",
            "logradouro": "Rua das Flores",
            "bairro": "Jardim das Américas",
            "numero": "100",
            "cep": "12345-678",
            "complemento": "Apto 12",
            "cidade": "Belo Horizonte",
            "uf": "MG",
            "observacao": "Funcionário responsável pela supervisão das operações agrícolas.",
            "usuario": self.user,
        }
        self.funcionario = Funcionario.objects.create(**self.funcionario_data)

    def test_get_lista(self):
        response = self.client.get(reverse("funcionario:get_lista"),
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}')
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.funcionario.nome)

    def test_get_detalhe(self):
        response = self.client.get(
            reverse("funcionario:get_detalhe", args=[self.funcionario.id]),
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.funcionario.nome)
        self.assertEqual(response.json()["nome"], self.funcionario_data["nome"])

    def test_put_editar(self):
        updated_data = {"nome": "Funcionario Atualizado"}
        response = self.client.put(
            reverse("funcionario:put_editar", args=[self.funcionario.pk]),
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',
            data=json.dumps(updated_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 200)
        self.funcionario.refresh_from_db()
        self.assertEqual(self.funcionario.nome, "Funcionario Atualizado")

    def test_get_detalhe_not_found(self):
        response = self.client.get(
            reverse("funcionario:get_detalhe", args=[999]),
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}'
        )  # ID que não existe
        self.assertEqual(response.status_code, 404)

    def test_put_editar_not_found(self):
        updated_data = {"nome": "Funcionario Atualizado"}
        response = self.client.put(
            reverse("funcionario:put_editar", args=[999]),
            HTTP_AUTHORIZATION=f'Bearer {self.access_token}',  # Ajuste o nome da URL
            data=json.dumps(updated_data),
            content_type="application/json",
        )
        self.assertEqual(response.status_code, 404)
