from django.urls import path, include

from .views import PaymentAPI

urlpatterns = [
    path('payment/make/', PaymentAPI.as_view(), name='make_payment')
]