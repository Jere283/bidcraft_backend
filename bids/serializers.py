from rest_framework import serializers

from products.serializers import GetAuctionSerializer
from users.serializers import UserRegisterSerializer
from .models import Bids, CompletedAuctions
from products.models import Auction
from users.models import User
from django.utils import timezone


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
