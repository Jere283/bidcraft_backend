
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
        read_only_fields = ['auction_id', 'date_listed', 'is_active', 'highest_bid', 'start_time']

    def validate(self, attrs):
        # Validation logic
        return attrs

    def create(self, validated_data):
        # Create logic
        return Auction.objects.create(**validated_data)


class CreateFavoritesSerializer(serializers.ModelSerializer):

    user = UserRegisterSerializer( read_only=True)
    auction = GetAuctionSerializer( read_only=True)

    class Meta:
        model = Favorites
        fields = ['favorite_id', 'user', 'auction', 'date_added']

    def validate(self, attrs):
        user = self.context['request'].user
        auction = self.context['auction_id']

        if Favorites.objects.filter(user=user, auction=auction).exists():
            raise serializers.ValidationError("This favorite already exists.")

        return attrs

    def create(self, validated_data):
        favorite =  Favorites.objects.create(
            user=self.context['request'].user,
            auction=self.context['auction_id'],
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

