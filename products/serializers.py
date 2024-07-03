from rest_framework import serializers
from .models import Category, Product, Favorites
from users.models import User

class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'category_name']

class ProductSerializer(serializers.ModelSerializer):
    seller = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='user_id'
    )
    category = serializers.SlugRelatedField(
        queryset=Category.objects.all(),
        slug_field='category_name',
        allow_null=True,
        required=False
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
            'date_listed',
            'is_active',
            'is_auction'
        ]
        read_only_fields = ['product_id']

class FavoritesSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='user_id'
    )
    product = serializers.SlugRelatedField(
        queryset=Product.objects.all(),
        slug_field='name',
        allow_null=True,
        required=False
    )
    class Meta:
        model = Favorites
        fields = ['favorite_id', 'user', 'product', 'date_added']