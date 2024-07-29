# auctions/management/commands/update_auction_statuses.py

from django.core.management.base import BaseCommand
from django.utils import timezone
from products.models import Auction

class Command(BaseCommand):
    help = 'Update auction statuses to inactive if end time has passed'

    def handle(self, *args, **kwargs):
        now = timezone.now()
        auctions = Auction.objects.filter(end_time__lte=now, is_active=True)
        count = auctions.update(is_active=False)
        self.stdout.write(self.style.SUCCESS(f'Successfully updated {count} auctions'))
