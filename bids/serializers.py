from rest_framework import serializers

from products.serializers import GetAuctionSerializer, GetAuctionImageSerializer
from users.serializers import UserRegisterSerializer
from .models import Bids, CompletedAuctions, SellerReviews, Notifications
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


