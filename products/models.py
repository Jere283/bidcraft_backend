from django.db import models #definir modelos de la BD
from users.models import users,CustomUserManager #importa modelos

#CREANDO DOS MODELOS CATEGORY y PRODUCT

#CREANDO MODEL CATEGORY
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)  # Se generará automáticamente
    category_name = models.CharField(max_length=50, unique=True)

    class Meta:
        db_table = 'categories'
        managed = False

    def __str__(self): #para devolver el nombre de la categoría cuando se convierta el objeto a una cadena.
        return self.category_name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)  # Se generará automáticamente
    seller = models.ForeignKey(users, on_delete=models.CASCADE)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2)
    buy_it_now_price = models.DecimalField(max_digits=10, decimal_places=2)
    quantity = models.IntegerField(default=1)
    category = models.ForeignKey(Category, on_delete=models.SET_NULL, null=True)
    date_listed = models.DateTimeField(auto_now_add=True)

    class Meta:
        db_table = 'products'
        managed = False

    def __str__(self):
        return self.name
