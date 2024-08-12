from rest_framework import serializers

from products.serializers import GetAuctionSerializer, GetAuctionImageSerializer, AuctionSerializer
from users.serializers import UserRegisterSerializer
from .models import Bids, CompletedAuctions, SellerReviews, Notifications, Purchases
from products.models import Auction, AuctionImage
from users.models import User
from django.utils import timezone


class GetBidSerializer(serializers.ModelSerializer):
    bidder = UserRegisterSerializer(read_only=True)
    class Meta:
        model = Bids
        fields = ['bid_id', 'bidder', 'auction', 'bid_time', 'bid_amount']

class CreateBidSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bids
        fields = ['bid_amount', 'bid_time']

    def validate(self, attrs):
        auction = Auction.objects.get(auction_id=self.context['auction_id'])

        if auction.is_active is False:
            raise serializers.ValidationError("La subasta ya finalizo")

        return attrs

    def create(self, validated_data):
        auction_id = self.context['auction_id']
        bid = Bids.objects.create(
            auction_id=auction_id,
            bidder=self.context['request'].user,
            bid_amount=validated_data['bid_amount'],
            bid_time=timezone.now()
        )
        return bid


class CompletedAuctionSerializer(serializers.ModelSerializer):
    buyer = UserRegisterSerializer(read_only=True)
    auction = GetAuctionSerializer(read_only=True)
    class Meta:
        model = CompletedAuctions
        fields = ['completed_auction_id', 'auction', 'buyer', 'highest_bid', 'is_paid', 'date_completed']


class NotificationAuctionSerializer(serializers.ModelSerializer):
    images = GetAuctionImageSerializer(many=True, source='auctionimage_set')

    class Meta:
        model = Auction
        fields = ('auction_id', 'name', 'description', 'highest_bid', 'images')

    def get_images(self, obj):
        images = AuctionImage.objects.filter(auction=obj)
        return GetAuctionImageSerializer(images, many=True).data


class SellerReviewsSerializer(serializers.ModelSerializer):
    class Meta:
        model = SellerReviews
        fields = ['review_id', 'buyer', 'seller', 'auction', 'rating', 'comment', 'review_date']
        read_only_fields = ['review_id', 'buyer', 'review_date']

    def validate_rating(self, value):
        if value < 1 or value > 5:
            raise serializers.ValidationError("El puntaje debe estar entre 1 y 5.")
        return value


class GetNotificationsSerializer(serializers.ModelSerializer):

    related_auction = NotificationAuctionSerializer(read_only=True)
    class Meta:
        model = Notifications
        fields = ['notification_id', 'message', 'related_auction', 'is_read']
        read_only_fiedls = ['notification_id', 'message', 'related_auction', 'is_read']


class PurchasesSerializer(serializers.ModelSerializer):
    seller = UserRegisterSerializer()
    buyer = UserRegisterSerializer()
    auction = GetAuctionSerializer()

    class Meta:
        model = Purchases
        fields = ['purchase_id', 'seller', 'buyer', 'auction', 'purchase_date', 'total_amount']

    def to_representation(self, instance):
        representation = super().to_representation(instance)
        auction_data = representation['auction']

        # Elimina los campos innecesarios del detalle de la subasta
        auction_fields_to_remove = ['seller', 'starting_price', 'buy_it_now_price',
                                    'date_listed', 'is_active', 'highest_bid',
                                    'start_time', 'end_time', 'winner']
        for field in auction_fields_to_remove:
            auction_data.pop(field, None)

        representation['auction'] = auction_data
        return representation

