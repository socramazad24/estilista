"""
User manager for estilera project.
"""
from django.contrib.auth.models import BaseUserManager


class UserManager(BaseUserManager):
    def create_user(self, username, email, first_name, last_name, password=None, **extra_fields):
        if not username:
            raise ValueError('El usuario es obligatorio')
        if not email:
            raise ValueError('El correo electrónico es obligatorio')
        if not first_name:
            raise ValueError('El nombre es obligatorio')
        if not last_name:
            raise ValueError('El apellido es obligatorio')
        
        email = self.normalize_email(email)
        user = self.model(
            username=username,
            email=email,
            first_name=first_name,
            last_name=last_name,
            **extra_fields
        )
        user.set_password(password)
        user.save(using=self._db)
        return user
    
    def create_superuser(self, username, email, first_name, last_name, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)
        extra_fields.setdefault('role', 'admin')
        
        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')
        
        return self.create_user(username, email, first_name, last_name, password, **extra_fields)
