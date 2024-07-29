from django.db import models #definir modelos de la BD
from users.models import User,CustomUserManager #importa modelos

class Category(models.Model):
    category_id = models.AutoField(primary_key=True)
    category_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'categories'

    def create_category(category_name, **extra_fields):
        if not category_name:
            raise ValueError('Se necesita un nombre de categoría')

        category = Category(category_name=category_name, **extra_fields)
        category.save()

        return category


class Status(models.Model):
    status_id = models.AutoField(primary_key=True)
    name = models.CharField(unique=True, max_length=30)

    class Meta:
        managed = False
        db_table = 'statuses'


class Auction(models.Model):
    auction_id = models.AutoField(primary_key=True)
    seller = models.ForeignKey(User, models.DO_NOTHING)
    name = models.CharField(max_length=100)
    description = models.TextField(blank=True, null=True)
    starting_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    buy_it_now_price = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    category = models.ForeignKey(Category, models.DO_NOTHING, blank=True, null=True)
    date_listed = models.DateTimeField(blank=True, null=True)
    is_active = models.BooleanField(blank=True, null=True)
    highest_bid = models.DecimalField(max_digits=10, decimal_places=2, blank=True, null=True)
    start_time = models.DateTimeField(blank=True, null=True)
    end_time = models.DateTimeField(blank=True, null=True)
    winner = models.ForeignKey(User, models.DO_NOTHING, related_name='auctions_winner_set', blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auctions'


class AuctionsStatuses(models.Model):
    product_status_id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, models.DO_NOTHING)
    status = models.ForeignKey(Status, models.DO_NOTHING)
    status_change_date = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auctions_statuses'


class Favorites(models.Model):
    favorite_id = models.AutoField(primary_key=True)
    user = models.ForeignKey(User, models.DO_NOTHING)
    auction = models.ForeignKey(Auction, models.DO_NOTHING)
    date_added = models.DateTimeField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'favorites'
        unique_together = (('user', 'auction'),)


class AuctionImage(models.Model):
    image_id = models.AutoField(primary_key=True)
    auction = models.ForeignKey(Auction, models.DO_NOTHING)
    image_url = models.CharField(max_length=255)

    class Meta:
        managed = False
        db_table = 'auction_images'

class Tags(models.Model):
    tag_id = models.AutoField(primary_key=True)
    tag_name = models.CharField(max_length=50)

    class Meta:
        managed = False
        db_table = 'tags'

class AuctionsTags(models.Model):
    auction_tags_id = models.AutoField(primary_key=True)
    tag = models.ForeignKey('Tags', models.DO_NOTHING, blank=True, null=True)
    auction = models.ForeignKey(Auction, models.DO_NOTHING, blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'auctions_tags'
