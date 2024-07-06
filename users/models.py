from django.contrib.auth.models import AbstractBaseUser, BaseUserManager, PermissionsMixin
from django.core.validators import validate_email
from django.core.exceptions import ValidationError
from django.db import models
from rest_framework_simplejwt.tokens import RefreshToken


class CustomUserManager(BaseUserManager):

    def email_validator(self, email):
        try:
            validate_email(email)
        except ValidationError:
            raise ValueError("Ingresa un correo electronico valido")

    def create_user(self, user_id, email, first_name, last_name, username, password, **extra_fields):
        if not email:
            raise ValueError('Se necesita un correo electronico')
        email = self.normalize_email(email)
        self.email_validator(email)

        if not first_name:
            raise ValueError('Se necesita un primer nombre')
        if not last_name:
            raise ValueError('Se necesita un apellido')

        user = self.model(user_id=user_id, email=email, username=username, first_name=first_name,
                          last_name=last_name, **extra_fields)
        user.set_password(password)
        user.save(using=self._db)

        return user

    def create_superuser(self, user_id, email, first_name, last_name, username=None, password=None, **extra_fields):
        extra_fields.setdefault('is_staff', True)
        extra_fields.setdefault('is_superuser', True)

        if extra_fields.get('is_staff') is not True:
            raise ValueError('Superuser must have is_staff=True.')
        if extra_fields.get('is_superuser') is not True:
            raise ValueError('Superuser must have is_superuser=True.')

        user = self.create_user(
            user_id, email, first_name, last_name, username, password, **extra_fields
        )
        user.save(using=self._db)

        return user



class Countries(models.Model):
    country_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=80)

    class Meta:
        managed = False
        db_table = 'countries'


class Departments(models.Model):
    department_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)
    country = models.ForeignKey(Countries, models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'departments'

class Cities(models.Model):
    city_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=80)
    department = models.ForeignKey('Departments', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'cities'
        unique_together = (('name', 'department'),)

class Addresses(models.Model):
    address_id = models.AutoField(primary_key=True)
    name = models.CharField(max_length=200)
    city = models.ForeignKey('Cities', models.DO_NOTHING)

    class Meta:
        managed = False
        db_table = 'addresses'


class User(AbstractBaseUser, PermissionsMixin):
    id = models.CharField(max_length=20, unique=True, primary_key=True)
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
    address = models.ForeignKey(Addresses, models.DO_NOTHING, blank=True, null=True)
    otp_verified = models.BooleanField(blank=True, null=True)

    objects = CustomUserManager()

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = ['id', 'first_name', 'last_name', 'username']

    class Meta:
        db_table = 'users'

    def __str__(self):
        return self.id

    @property
    def get_full_name(self):
        return f"{self.first_name} {self.last_name}"


    def tokens(self):
        refresh = RefreshToken.for_user(self)
        return {
            'refresh': str(refresh),
            'access': str(refresh.access_token)
        }


class Otps(models.Model):
    user = models.ForeignKey(User, models.DO_NOTHING, blank=True, null=True, unique=True)
    code = models.CharField(max_length=6, unique=True)

    class Meta:
        db_table = 'otps'
    def __str__(self):
        return f"{self.user.first_name}--passcode"


