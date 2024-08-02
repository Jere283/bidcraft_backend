from django.urls import path, include

from .views import PaymentAPI

urlpatterns = [
    path('payment/make/<int:auction_id>/', PaymentAPI.as_view(), name='make_payment')
]