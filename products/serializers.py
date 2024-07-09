from rest_framework import serializers
from .models import Category, Auction, Favorites, Status
from users.models import User
from users.serializers import LoginSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'category_name']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('status_id', 'name')


class AuctionSerializer(serializers.ModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)
    winner = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), allow_null=True, write_only=True)

    class Meta:
        model = Auction
        fields = ('auction_id', 'seller', 'name', 'description', 'starting_price', 'buy_it_now_price',
                  'category', 'date_listed', 'is_active', 'highest_bid', 'start_time', 'end_time', 'winner')
        read_only_fields = ['auction_id']

    def validate(self, attrs):
        if attrs.get('starting_price') and attrs.get('buy_it_now_price') and attrs['starting_price'] > attrs['buy_it_now_price']:
            raise serializers.ValidationError("Starting price cannot be higher than buy it now price.")
        return attrs

    def create(self, validated_data):
        auction = Auction.objects.create(
            seller=validated_data['seller'],
            name=validated_data['name'],
            description=validated_data.get('description', ''),
            starting_price=validated_data.get('starting_price', None),
            buy_it_now_price=validated_data.get('buy_it_now_price', None),
            category=validated_data.get('category', None),
            date_listed=validated_data.get('date_listed', None),
            is_active=validated_data.get('is_active', True),
            highest_bid=validated_data.get('highest_bid', None),
            start_time=validated_data.get('start_time', None),
            end_time=validated_data.get('end_time', None),
            winner=validated_data.get('winner', None),
        )
        return auction


class FavoritesSerializer(serializers.ModelSerializer):
    user = serializers.SlugRelatedField(
        queryset=User.objects.all(),
        slug_field='id'
    )
    auction = serializers.SlugRelatedField(
        queryset=Auction.objects.all(),
        slug_field='auction_id',
        allow_null=True,
        required=False
    )

    class Meta:
        model = Favorites
        fields = ['favorite_id', 'user', 'auction', 'date_added']
