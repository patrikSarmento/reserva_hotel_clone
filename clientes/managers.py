from django.contrib.auth.base_user import BaseUserManager

class CustomUserManager(BaseUserManager):
    def create_user(self, email, nome, cpf, password=None):
        if not email:
            raise ValueError('Usuário precisa ter um email válido')
        email = self.normalize_email(email)
        user = self.model(email=email, nome=nome, cpf=cpf)
        user.set_password(password)  # seta a senha com hash
        user.save(using=self._db)
        return user

    def create_superuser(self, email, nome, cpf, password):
        user = self.create_user(email, nome, cpf, password)
        user.is_staff = True
        user.is_superuser = True
        user.save(using=self._db)
        return user
