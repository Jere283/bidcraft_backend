from django.db import models #definir modelos de la BD
from users.models import User,CustomUserManager #importa modelos

#CREANDO DOS MODELOS CATEGORY y PRODUCT

#CREANDO MODEL CATEGORY
class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'categories'


    def __str__(self): #para devolver el nombre de la categoría cuando se convierta el objeto a una cadena.
        return self.category_name

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    seller_id = models.CharField(max_length=14)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    buy_it_now_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    quantity = models.IntegerField(blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    date_listed = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    is_auction = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'products'

