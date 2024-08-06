from django.shortcuts import get_object_or_404
from rest_framework.permissions import IsAuthenticated
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
import stripe

from bids.models import CompletedAuctions
from products.models import Auction
from .serializers import PaymentSerializer
from products.serializers import GetAuctionSerializer

class PaymentAPI(APIView):
    def post(self, request, auction_id):
        serializer = PaymentSerializer(data=request.data)
        if serializer.is_valid():
            token = serializer.validated_data.get('token')
            amount = serializer.validated_data.get('amount')
            currency = serializer.validated_data.get('currency')
            description = serializer.validated_data.get('description', '')

            stripe.api_key = 'sk_test_51PhHbiRxcO9tjCUh5aJpo0BOSXy9KbP1Tg9z3CO2bRJ5JVfOgQ1Al0cGZapzkRByxSDZtSlRQiuQ3eW4ZAclw6ar00rtvboxY6'

            try:
                # Create a PaymentIntent with the tokenized card details
                payment_intent = stripe.PaymentIntent.create(
                    amount=amount,  # amount in cents
                    currency=currency,
                    description=description,
                    payment_method_data={
                        'type': 'card',
                        'card': {
                            'token': token,
                        },
                    },
                    confirm=True,
                    automatic_payment_methods={
                        'enabled': True,
                        'allow_redirects': 'never'
                    }
                )

                if payment_intent['status'] == 'succeeded':
                    auction = CompletedAuctions.objects.get(auction=auction_id)
                    auction.is_paid = True
                    auction.save()
                    response = {
                        'message': "Card Payment Success",
                        'status': status.HTTP_200_OK,
                        "payment_intent": payment_intent
                    }
                else:
                    response = {
                        'message': "Card Payment Failed",
                        'status': status.HTTP_400_BAD_REQUEST,
                        "payment_intent": payment_intent
                    }
            except stripe.error.CardError as e:
                response = {
                    'error': "Card error: {}".format(e.user_message),
                    'status': status.HTTP_400_BAD_REQUEST,
                    "payment_intent": {"id": "Null"},
                }
            except stripe.error.StripeError as e:
                response = {
                    'error': "Stripe error: {}".format(e.user_message),
                    'status': status.HTTP_400_BAD_REQUEST,
                    "payment_intent": {"id": "Null"},
                }
            except Exception as e:
                response = {
                    'error': "Unknown error: {}".format(str(e)),
                    'status': status.HTTP_400_BAD_REQUEST,
                    "payment_intent": {"id": "Null"},
                }

            return Response(response)
        else:
            return Response(
                {'errors': serializer.errors},
                status=status.HTTP_400_BAD_REQUEST
            )


class BuyItNowClass(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetAuctionSerializer
    def post(self, request, auction_id):
        auction = get_object_or_404(Auction, pk=auction_id, is_active=True)


        if auction.buy_it_now_price is None:
            return Response({'error': 'La subasta no tiene precio de comprar ahora'}, status=400)

        # Turn off the auction
        auction.is_active = False
        auction.winner = request.user
        auction.save()

        return Response({'message': 'La subasta fue comprada de manera exitosa'}, status=200)



