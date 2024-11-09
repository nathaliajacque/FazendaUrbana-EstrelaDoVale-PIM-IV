from utils.statusmodel import StatusModel
from django.contrib.auth.models import (
    AbstractBaseUser,
    BaseUserManager,
    PermissionsMixin,
)
from django.db import models
from PIL import Image
import os
from django.conf import settings


""" Usuario é o modelo que representa os usuários no sistema, 
enquanto CustomUserManager é o gerenciador de modelos que lida com a criação e manipulação 
de instâncias do modelo Usuario. Eles trabalham juntos para fornecer uma estrutura completa de 
autenticação e gerenciamento de usuários no Django.	"""


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email deve ser preenchido")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # # super usuário para acessar o django admin
    def create_superuser(self, email, password=None, **extra_fields):
        extra_fields.setdefault("is_staff", True)
        extra_fields.setdefault("is_superuser", True)

        if extra_fields.get("is_staff") is not True:
            raise ValueError("Superuser deve ter is_staff=True.")
        if extra_fields.get("is_superuser") is not True:
            raise ValueError("Superuser deve ter is_superuser=True.")

        return self.create_user(email, password, **extra_fields)


class Usuario(StatusModel, AbstractBaseUser, PermissionsMixin):
    PERFIL_CHOICES = [
        ("ADMINISTRADOR", "Administrador"),
        ("GERENTE", "Gerente"),
        ("FUNCIONARIO", "Funcionário"),
    ]

    name = models.CharField(max_length=255, blank=True)
    email = models.EmailField(unique=True)
    nivel_acesso = models.CharField(
        max_length=20, choices=PERFIL_CHOICES, default="FUNCIONARIO"
    )
    data_cadastro = models.DateTimeField(auto_now_add=True, editable=False)
    deve_redefinir_senha = models.BooleanField(default=False)
    is_staff = models.BooleanField(default=False)

    objects = CustomUserManager()

    USERNAME_FIELD = "email"
    REQUIRED_FIELDS = []

    def is_administrador(self):
        return self.nivel_acesso == "ADMINISTRADOR"

    def is_gerente(self):
        return self.nivel_acesso == "GERENTE"

    def is_funcionario(self):
        return self.nivel_acesso == "FUNCIONARIO"

    def __str__(self):
        return self.email

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
