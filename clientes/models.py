from django.db import models
from django.contrib.auth.models import AbstractBaseUser, PermissionsMixin
from django.utils import timezone
from django.core.exceptions import ValidationError
from django.contrib.auth.base_user import BaseUserManager
import re

# -----------------------
# Validação de CPF
# -----------------------
def validar_cpf(cpf):
    cpf = re.sub(r'[^0-9]', '', cpf)

    if len(cpf) != 11:
        raise ValidationError("CPF deve conter 11 números.")
    if cpf == cpf[0] * 11:
        raise ValidationError("CPF inválido.")

    soma = sum(int(cpf[i]) * (10 - i) for i in range(9))
    digito1 = (soma * 10) % 11
    if digito1 == 10:
        digito1 = 0
    if digito1 != int(cpf[9]):
        raise ValidationError("CPF inválido.")

    soma = sum(int(cpf[i]) * (11 - i) for i in range(10))
    digito2 = (soma * 10) % 11
    if digito2 == 10:
        digito2 = 0
    if digito2 != int(cpf[10]):
        raise ValidationError("CPF inválido.")

# -----------------------
# Gerenciador do CustomUser
# -----------------------
class CustomUserManager(BaseUserManager):
    def create_user(self, email, nome, cpf, password=None):
        if not email:
            raise ValueError("O usuário precisa de um email")
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, cpf=cpf)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, cpf, password):
        user = self.create_user(email=email, nome=nome, cpf=cpf, password=password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user

# -----------------------
# Modelo Customizado de Usuário
# -----------------------
class CustomUser(AbstractBaseUser, PermissionsMixin):
    nome = models.CharField(max_length=150)
    email = models.EmailField(unique=True)
    cpf = models.CharField(max_length=14, unique=True, validators=[validar_cpf])
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    date_joined = models.DateTimeField(default=timezone.now)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['nome', 'cpf']

    def __str__(self):
        return self.email

# -----------------------
# Modelo de Reserva
# -----------------------
class Reserva(models.Model):
    cliente = models.ForeignKey(CustomUser, on_delete=models.CASCADE)
    quarto = models.CharField(max_length=100)
    dias = models.PositiveIntegerField()
    data_reserva = models.DateTimeField(auto_now_add=True)

    def __str__(self):
        return f"{self.cliente.nome} - {self.quarto} ({self.dias} dias)"
