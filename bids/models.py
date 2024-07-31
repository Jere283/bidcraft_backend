from django.db import models

from products.models import Auction
from users.models import User


class Bids(models.Model):
    bid_id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, models.DO_NOTHING)
    bidder = models.ForeignKey(User, models.DO_NOTHING)
    bid_amount = models.DecimalField(max_digits=10, decimal_places=2)
    bid_time = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'bids'

class CompletedAuctions(models.Model):
    completed_auction_id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, models.DO_NOTHING)
    buyer = models.ForeignKey(User, models.DO_NOTHING)
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2)
    is_paid = models.BooleanField(blank=True, null=True)
    date_completed = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'completed_auctions'
