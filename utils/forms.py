import random
import string
from django import forms
from usuario.models import Usuario


class UsuarioAdminForm(forms.ModelForm):
    nova_senha = forms.CharField(
        label="Nova Senha", widget=forms.PasswordInput, required=False
    )

    class Meta:
        model = Usuario
        fields = "__all__"

    def save(self, commit=True):
        usuario = super().save(commit=False)
        nova_senha = self.cleaned_data.get("nova_senha")
        if not nova_senha:
            nova_senha = "".join(
                random.choices(string.ascii_letters + string.digits, k=8)
            )
            usuario.set_password(nova_senha)
            usuario.deve_redefinir_senha = True
        if commit:
            usuario.save()
        return usuario
