from django.urls import path, include

from bids.views import MakeABid, UserCompletedAuctionsView, CreateSellerReviewView, SellerReviewListView, \
    SellerReviewByAuctionView, UpdateSellerReviewView, DeleteSellerReviewView, SellerReviewsBySellerView

urlpatterns = [
    path('bids/create/one/<int:auction_id>/', MakeABid.as_view(), name='create_bid'),
    path('auctions/win/', UserCompletedAuctionsView.as_view(), name='user-completed-auctions'),

    #SellerReview
    path('review/create/<int:auction_id>/', CreateSellerReviewView.as_view(), name='create-seller-review'),
    path('reviews/show/all/', SellerReviewListView.as_view(), name='seller-review-list'),
    #path('reviews/auction/<int:auction_id>/', SellerReviewByAuctionView.as_view(), name='seller-review-by-auction'),
    path('reviews/auction/update/<int:auction_id>/', UpdateSellerReviewView.as_view(), name='update-seller-review'),
    path('reviews/auction/delete/<int:auction_id>/', DeleteSellerReviewView.as_view(), name='delete-seller-review'),
    path('reviews/seller/<str:seller_id>/', SellerReviewsBySellerView.as_view(), name='seller-reviews-by-seller'),
 ]