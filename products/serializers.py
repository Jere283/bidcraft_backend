from rest_framework import serializers
from .models import Category, Product
from users.models import users

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'category_name']
        read_only_fields = ('created_at', ) # Define que el campo created_at del modelo Category es de solo lectura y no se incluirá en los datos de entrada para la actualización.

class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(
        queryset=users.objects.all(),
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
