from rest_framework import serializers
from .models import Bids
from products.models import Auction
from users.models import User
from django.utils import timezone


class CreateBidSerializer(serializers.ModelSerializer):

    class Meta:
        model = Bids
        fields = ['bid_amount', 'bid_time']

    def create(self, validated_data):
        auction_id = self.context['auction_id']
        bid = Bids.objects.create(
            auction_id=auction_id,
            bidder=self.context['request'].user,
            bid_amount=validated_data['bid_amount'],
            bid_time=timezone.now()
        )
        return bid