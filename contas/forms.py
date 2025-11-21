from django import forms
from django.contrib.auth.models import User

class RegisterForm(forms.ModelForm):
    password = forms.CharField(
        label="Senha",
        widget=forms.PasswordInput
    )
    password2 = forms.CharField(
        label="Confirmar senha",
        widget=forms.PasswordInput
    )

    class Meta:
        model = User
        fields = ["username", "email", "password"]

        labels = {
            'username': 'Nome de usuário',
            'email': 'Email',
        }

        help_texts = {
            'username': 'Escolha um nome de usuário curto e fácil de lembrar.',
            'password': 'Sua senha deve ser segura.',
        }

    def clean(self):
        cleaned_data = super().clean()
        p1 = cleaned_data.get("password")
        p2 = cleaned_data.get("password2")

        if p1 and p2 and p1 != p2:
            self.add_error("password2", "As senhas não coincidem.")

        return cleaned_data
