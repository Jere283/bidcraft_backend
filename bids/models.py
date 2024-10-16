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


class SellerReviews(models.Model):
    review_id = models.AutoField(primary_key=True)
    buyer = models.ForeignKey(User, models.DO_NOTHING)
    seller = models.ForeignKey(User, models.DO_NOTHING, related_name='sellerreviews_seller_set')
    auction = models.ForeignKey(Auction, models.DO_NOTHING)
    rating = models.IntegerField()
    comment = models.TextField(blank=True, null=True)
    review_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'seller_reviews'


class Notifications(models.Model):
    notification_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    message = models.TextField()
    related_auction = models.ForeignKey(Auction, models.DO_NOTHING, blank=True, null=True)
    is_read = models.BooleanField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'notifications'


class Purchases(models.Model):
    purchase_id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(User, models.DO_NOTHING)
    buyer = models.ForeignKey(User, models.DO_NOTHING, related_name='purchases_buyer_set')
    auction = models.ForeignKey(Auction, models.DO_NOTHING)
    purchase_date = models.DateTimeField(blank=True, null=True)
    total_amount = models.DecimalField(max_digits=10, decimal_places=2)

    class Meta:
        managed = False
        db_table = 'purchases'
