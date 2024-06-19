from django.db import models


class Role(models.Model):
    id_role = models.AutoField(primary_key=True)
    role = models.CharField(max_length=40, unique=True)

    class Meta:
        managed = False
        ordering = ['role']
        db_table = 'roles'

    def __str__(self):
        return self.role



class User(models.Model):
    id_user = models.AutoField(primary_key=True)
    names = models.CharField(max_length=150)
    last_names = models.CharField(max_length=150)
    id_number = models.CharField(max_length=14, unique=True)
    date_of_birth = models.DateField()
    email = models.EmailField(max_length=110, unique=True)
    password = models.CharField(max_length=150)
    id_role = models.ForeignKey(Role, db_column='id_role', on_delete=models.SET_NULL, null=True, default=None)

    class Meta:
        managed = False
        ordering = ['id_number', 'email']
        db_table = 'users'

    def __str__(self):
        return f"{self.names} {self.last_names}"
