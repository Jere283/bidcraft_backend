from rest_framework import serializers
from .models import Category, Product
from users.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'category_name']

class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='dni'
    )
    category = serializers.SlugRelatedField( #Indica que este campo también se representará como un campo de relación mediante un "slug".
        queryset=Category.objects.all(), #indica que todas las instancias del modelo Category están disponibles para seleccionar como categorías
        slug_field='category_name', #Indica que el campo category_name del modelo Category se utilizará como identificador en lugar del ID de la categoría.
        allow_null=True, #significa que no es obligatorio seleccionar una categoría para un producto.
        required=False # Indica que este campo no es obligatorio durante la creación o actualización de un producto. Si no se proporciona, se permitirá que sea nulo (null)
    )

    class Meta:
        model = Product
        fields = [
            'product_id', 
            'seller', 
            'name', 
            'description', 
            'starting_price', 
            'buy_it_now_price', 
            'quantity', 
            'category', 
            'date_listed'
        ]
        read_only_fields = ('created_at', )
