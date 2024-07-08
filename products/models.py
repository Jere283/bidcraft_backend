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

def create_category(category_name, **extra_fields):
    if not category_name:
        raise ValueError('Se necesita un nombre de categoría')

    category = Category(category_name=category_name, **extra_fields)
    category.save()

    return category

class Product(models.Model):
    product_id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(User, models.DO_NOTHING)
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

class Favorites(models.Model):
    favorite_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    product = models.ForeignKey(Product, models.DO_NOTHING)
    date_added = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'favorites'



