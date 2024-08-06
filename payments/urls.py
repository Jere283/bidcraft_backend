from django.urls import path, include

from .views import PaymentAPI, BuyItNowClass

urlpatterns = [
    path('payment/make/<int:auction_id>/', PaymentAPI.as_view(), name='make_payment'),
    path('auction/buy/now/<int:auction_id>/', BuyItNowClass.as_view(), name='but_it_now')
]