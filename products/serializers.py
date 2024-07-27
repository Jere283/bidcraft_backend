
from django.utils import timezone
from rest_framework import serializers
from .models import Category, Auction, Favorites, Status, AuctionImage, Tags, AuctionsTags
from users.models import User
from users.serializers import LoginSerializer, UserRegisterSerializer


class CategorySerializer(serializers.ModelSerializer):
    class Meta:
        model = Category
        fields = ['category_id', 'category_name']


class StatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = Status
        fields = ('status_id', 'name')

class GetAuctionImageSerializer(serializers.ModelSerializer):
    class Meta:
        model = AuctionImage
        fields = ('image_id', 'image_url')


class GetAuctionSerializer(serializers.ModelSerializer):
    seller = UserRegisterSerializer()
    category = CategorySerializer()
    winner = UserRegisterSerializer()
    images = GetAuctionImageSerializer(many=True, source='auctionimage_set')

    class Meta:
        model = Auction
        fields = ('auction_id', 'seller', 'name', 'description', 'starting_price', 'buy_it_now_price',
                  'category', 'date_listed', 'is_active', 'highest_bid', 'start_time', 'end_time', 'winner',
                  'images')

    # Include any extra methods if necessary, for example:
    def get_images(self, obj):
        images = AuctionImage.objects.filter(auction=obj)
        return GetAuctionImageSerializer(images, many=True).data


class CreateAuctionSerializer(serializers.ModelSerializer):
    seller = serializers.PrimaryKeyRelatedField(queryset=User.objects.all(), write_only=True)
    category = serializers.PrimaryKeyRelatedField(queryset=Category.objects.all(), write_only=True)

    seller_detail = UserRegisterSerializer(source='seller', read_only=True)
    category_detail = CategorySerializer(source='category', read_only=True)
    winner_detail = UserRegisterSerializer(source='winner', read_only=True)

    class Meta:
        model = Auction
        fields = ('auction_id', 'seller', 'name', 'description', 'starting_price', 'buy_it_now_price',
                  'category', 'date_listed', 'is_active', 'highest_bid', 'start_time', 'end_time',
                  'seller_detail', 'category_detail', 'winner_detail')
        read_only_fields = ['auction_id', 'date_listed', 'is_active', ' highest_bid', 'start_time']

    def validate(self, attrs):
        if attrs.get('starting_price') and attrs.get('buy_it_now_price') and attrs['starting_price'] > attrs[
            'buy_it_now_price']:
            raise serializers.ValidationError("El precio inicial no puede ser mayor al precio de comprar ahora.")

        start_time = attrs.get('start_time', None)
        end_time = attrs.get('end_time', None)

        if start_time and start_time.tzinfo is None:
            start_time = timezone.make_aware(start_time)
        if end_time and end_time.tzinfo is None:
            end_time = timezone.make_aware(end_time)

        if start_time and end_time and end_time <= start_time:
            raise serializers.ValidationError("El tiempo de finalizacion no puede ser igual o menor al tiempo de inicio.")

        if end_time and end_time <= timezone.now():
            raise serializers.ValidationError("La subasta no puede terminar en el pasado.")

        return attrs


    def create(self, validated_data):
        auction = Auction.objects.create(
            seller=validated_data['seller'],
            name=validated_data['name'],
            description=validated_data.get('description', ''),
            starting_price=validated_data.get('starting_price'),
            highest_bid=validated_data.get('starting_price'),
            buy_it_now_price=validated_data.get('buy_it_now_price'),
            category=validated_data.get('category'),
            date_listed=validated_data.get('date_listed',  timezone.now()),
            is_active=validated_data.get('is_active', True),
            start_time=validated_data.get('start_time', timezone.now()),
            end_time=validated_data.get('end_time', None),
        )
        return auction


class CreateFavoritesSerializer(serializers.ModelSerializer):

    user = UserRegisterSerializer( read_only=True)
    auction = GetAuctionSerializer( read_only=True)

    class Meta:
        model = Favorites
        fields = ['favorite_id', 'user', 'auction', 'date_added']

    def validate(self, attrs):
        user = self.context['request'].user
        auction = self.context['auction']

        if Favorites.objects.filter(user=user, auction=auction).exists():
            raise serializers.ValidationError("This favorite already exists.")

        return attrs

    def create(self, validated_data):
        favorite =  Favorites.objects.create(
            user=self.context['request'].user,
            auction=self.context['auction'],
            date_added=timezone.now()
        )

        return favorite


class GetFavoriteSerializer(serializers.ModelSerializer):
    user = UserRegisterSerializer()
    auction = GetAuctionSerializer()

    class Meta:
        model = Favorites
        fields = ['favorite_id', 'user', 'auction', 'date_added']

class CreateImageForAuctionSerializer(serializers.ModelSerializer):
    auction = serializers.PrimaryKeyRelatedField(queryset=Auction.objects.all())

    class Meta:
        model = AuctionImage
        fields =['image_id', 'auction', 'image_url']

    def create(self, validated_data):
        image = AuctionImage.objects.create(
            auction = validated_data['auction'],
            image_url =validated_data['image_url']

        )
        return  image

class CreateTagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['tag_id', 'tag_name']

    def create(self, validated_data):
        tag = Tags.objects.create(
            tag_name=validated_data['tag_name']
        )
        return tag

class TagSerializer(serializers.ModelSerializer):
    class Meta:
        model = Tags
        fields = ['tag_id', 'tag_name']

class AuctionSerializer(serializers.ModelSerializer):
    class Meta:
        model = Auction
        fields = ['auction_id']

class AuctionsTagsSerializer(serializers.ModelSerializer):
    tag = serializers.PrimaryKeyRelatedField(queryset=Tags.objects.all())
    auction = serializers.PrimaryKeyRelatedField(queryset=Auction.objects.all())

    class Meta:
        model = AuctionsTags
        fields = ['auction_tags_id', 'tag', 'auction']

