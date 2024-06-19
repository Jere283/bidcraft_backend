from django.db import models


class Roles(models.Model):
    id_role = models.AutoField(primary_key=True)
    role = models.CharField(max_length=40, unique=True)

    class Meta:
        ordering = ['role']

    def __str__(self):
        return self.role


class Users(models.Model):
    id_user = models.AutoField(primary_key=True)
    names = models.CharField(max_length=150)
    last_names = models.CharField(max_length=150)
    id_number = models.CharField(max_length=14, unique=True)
    date_of_birth = models.DateField()
    email = models.EmailField(max_length=110, unique=True)
    password = models.CharField(max_length=150)
    id_role = models.ForeignKey(Role, on_delete=models.SET_NULL, null=True, default=None)

    class Meta:
        ordering = ['id_number', 'email']

    def __str__(self):
        return f"{self.names} {self.last_names}"
