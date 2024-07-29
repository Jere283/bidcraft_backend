from django.db import models

from users.models import User
from products.models import Auction
# Create your models here.

class KycStatus(models.Model):
    status_id = models.AutoField(primary_key=True)
    status = models.CharField(unique=True, max_length=50)

    class Meta:
        managed = False
        db_table = 'kyc_status'

class UsersKyc(models.Model):
    user = models.OneToOneField(User, models.DO_NOTHING, primary_key=True)
    front_id = models.CharField(max_length=200, blank=True, null=True)
    back_id = models.CharField(max_length=200, blank=True, null=True)
    profile_picture = models.CharField(max_length=200, blank=True, null=True)
    status = models.ForeignKey(KycStatus, models.DO_NOTHING, db_column='status', blank=True, null=True)
    comment = models.TextField(blank=True, null=True)

    class Meta:
        managed = False
        db_table = 'users_kyc'


