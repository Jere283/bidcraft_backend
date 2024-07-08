from django.contrib import admin

from .models import Auction, Status, AuctionsStatuses, Bids, Favorites, Category


admin.site.register(Auction)
admin.site.register(Status)
admin.site.register(AuctionsStatuses)
admin.site.register(Bids)
admin.site.register(Favorites)
admin.site.register(Category)
