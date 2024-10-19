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


class CustomUserManager(BaseUserManager):
    def create_user(self, email, password=None, **extra_fields):
        if not email:
            raise ValueError("O email deve ser preenchido")
        email = self.normalize_email(email)
        user = self.model(email=email, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    # super usuário para acessar o django admin
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

    # Método para redimensionar a imagem do usuário
    # @staticmethod
    # def resize_image(img, new_width=800):
    #     img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
    #     img_pil = Image.open(img_full_path)
    #     original_width, original_height = img_pil.size

    #     if original_width <= new_width:
    #         print("Retornando")
    #         img_pil.close()
    #         return

    #     new_height = round(new_width * original_height / original_width)
    #     new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)

    # def save(self, *args, **kwargs):
    #     super().save(*args, **kwargs)

    #     max_image_size = 800

    #     if self.imagem:
    #         self.resize_image(self.imagem.path, max_image_size)
