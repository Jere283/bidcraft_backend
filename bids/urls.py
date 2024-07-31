from django.urls import path, include

from bids.views import MakeABid, UserCompletedAuctionsView

urlpatterns = [
    path('bids/create/one/<int:auction_id>/', MakeABid.as_view(), name='create_bid'),
    path('auctions/win/', UserCompletedAuctionsView.as_view(), name='user-completed-auctions'),
 ]