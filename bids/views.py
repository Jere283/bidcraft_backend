from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404, ListAPIView
from products.models import Auction
from .models import CompletedAuctions
from .serializers import CreateBidSerializer, CompletedAuctionSerializer
from rest_framework.permissions import IsAuthenticated


class MakeABid(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateBidSerializer

    def post(self, request, auction_id):
        auction = get_object_or_404(Auction, pk=auction_id)

        serializer = self.serializer_class(
            data=request.data,
            context={'request': request, 'auction_id': auction_id}
        )

        try:
            if serializer.is_valid():
                serializer.save()
                return Response({
                    'data': serializer.data,
                    'message': "La puja fue hecha"
                }, status=status.HTTP_201_CREATED)
        except IntegrityError as e:
            error_message = str(e)
            if 'violates check constraint "check_highest_bid"' in error_message:
                return Response({'error': 'El monto de la puja debe ser mayor que la puja más alta actual.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Error de integridad en la base de datos.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class UserCompletedAuctionsView(ListAPIView):
    serializer_class = CompletedAuctionSerializer
    permission_classes = [IsAuthenticated]  # Ensure the user is authenticated

    def get_queryset(self):
        user = self.request.user
        return CompletedAuctions.objects.filter(buyer=user).order_by('completed_auction_id')