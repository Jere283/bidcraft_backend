from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.db import models

class CustomUserManager(BaseUserManager):
    def create_user(self, dni, email, username=None, password=None, **extra_fields):
        if not email:
            raise ValueError('Se necesita un correo electronico')
        email = self.normalize_email(email)
        user = self.model(dni=dni, email=email, username=username, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)
        return user

    def create_superuser(self, dni, email, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        return self.create_user(dni, email, username, password, **extra_fields)

class users(AbstractBaseUser, PermissionsMixin):
    dni = models.CharField(max_length=20, unique=True, primary_key=True)
    first_name = models.CharField(max_length=50)
    second_name = models.CharField(max_length=50, blank=True, null=True)
    last_name = models.CharField(max_length=50)
    last_name2 = models.CharField(max_length=50, blank=True, null=True)
    phone_number = models.CharField(max_length=20, blank=True, null=True)
    email = models.EmailField(unique=True)
    username = models.CharField(max_length=50, unique=True, blank=True, null=True)
    is_active = models.BooleanField(default=True)
    is_staff = models.BooleanField(default=False)
    is_superuser = models.BooleanField(default=False)
    last_login = models.DateTimeField(blank=True, null=True)
    date_joined = models.DateTimeField(auto_now_add=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'dni'
    EMAIL_FIELD = 'email'
    REQUIRED_FIELDS = ['email']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.dni
