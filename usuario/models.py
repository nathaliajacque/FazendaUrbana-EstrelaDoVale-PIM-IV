"""
Classe Usuario:
Adicionamos o campo nivel_acesso com as opções PERFIL_CHOICES.
Adicionamos métodos is_administrador, is_gerente e is_funcionario para verificar o nível de acesso do usuário.
Decoradores de Permissão:
Criamos decoradores administrador_required, gerente_required e funcionario_required para controlar o acesso às views com base no nível de acesso do usuário.
Uso nas Views:
Usamos os decoradores de permissão nas views para garantir que apenas usuários com o nível de acesso apropriado possam acessar determinadas funções.
"""

from django.contrib.auth.models import User
from utils.statusmodel import StatusModel
from django.db import models
from PIL import Image
import os
from django.conf import settings


# class UsuarioManager(BaseUserManager):
#     def create_user(self, login, nome, password=None, **extra_fields):
#         if not login:
#             raise ValueError("O campo login deve ser preenchido")
#         usuario = self.model(login=login, nome=nome, **extra_fields)
#         usuario.set_password(password)
#         usuario.save(using=self._db)
#         return usuario

#     def create_superuser(self, login, nome, password=None, **extra_fields):
#         extra_fields.setdefault("is_staff", True)
#         extra_fields.setdefault("is_superuser", True)
#         return self.create_user(login, nome, password, **extra_fields)


class Usuario(StatusModel):
    PERFIL_CHOICES = [
        ("", "Selecione o acesso"),
        ("administrador", "Administrador"),
        ("gerente", "Gerente"),
        ("funcionario", "Funcionário"),
    ]

    # Removido CPF e RG do campo de login
    # cpf = models.CharField(max_length=11, unique=True)
    # rg = models.CharField(max_length=20, unique=True)
    id_usuario = models.AutoField(primary_key=True)
    usuario = models.OneToOneField(User, on_delete=models.SET_NULL, null=True)
    nome = models.CharField(max_length=255)
    login = models.EmailField(max_length=255, unique=True)
    senha = models.CharField(max_length=255)
    nivel_acesso = models.CharField(max_length=20, choices=PERFIL_CHOICES)
    data_cadastro = models.DateTimeField(auto_now_add=True, editable=False)
    deve_redefinir_senha = models.BooleanField(default=False)

    @classmethod
    def create_usuario(cls, **kwargs):
        usuario = cls(**kwargs)
        usuario.save()
        return usuario

    @classmethod
    def get_usuario(cls, id_usuario):
        try:
            usuario = cls.objects.get(id_usuario=id_usuario)
            return {
                "id_usuario": usuario.id_usuario,
                "data_cadastro": usuario.data_cadastro,
                "nome": usuario.nome,
                "login": usuario.login,
                "nivel_acesso": usuario.nivel_acesso,
            }
        except cls.DoesNotExist:
            return None

    def is_administrador(self):
        return self.nivel_acesso == "administrador"

    def is_gerente(self):
        return self.nivel_acesso == "gerente"

    def is_funcionario(self):
        return self.nivel_acesso == "funcionario"

    @classmethod
    def update_usuario(cls, id_usuario, **kwargs):
        try:
            usuario = cls.objects.get(id_usuario=id_usuario)
            for key, value in kwargs.items():
                setattr(usuario, key, value)
            usuario.save()
            return usuario
        except cls.DoesNotExist:
            return None

    # Método para redimensionar a imagem do usuário
    @staticmethod
    def resize_image(img, new_width=800):
        img_full_path = os.path.join(settings.MEDIA_ROOT, img.name)
        img_pil = Image.open(img_full_path)
        original_width, original_height = img_pil.size

        if original_width <= new_width:
            print("Retornando")
            img_pil.close()
            return

        new_height = round(new_width * original_height / original_width)
        new_img = img_pil.resize((new_width, new_height), Image.LANCZOS)

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)

        max_image_size = 800

        if self.imagem:
            self.resize_image(self.imagem.path, max_image_size)

    def __self__(self):
        return f"{self.usuario}"

    def clean(self):
        pass

    class Meta:
        verbose_name = "Usuário"
        verbose_name_plural = "Usuários"
