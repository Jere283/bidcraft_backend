from django.urls import path, include

from bids.views import MakeABid

urlpatterns = [
    path('bids/create/one/<int:auction_id>/', MakeABid.as_view(), name='create_bid'),
 ]