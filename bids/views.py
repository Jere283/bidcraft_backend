from psycopg2 import IntegrityError, InternalError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404
from rest_framework.permissions import IsAuthenticated

from products.models import Auction
from .serializers import CreateBidSerializer


class MakeABid(GenericAPIView):
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
            # Customize error response based on the specific IntegrityError
            error_message = str(e)
            if 'violates check constraint "check_highest_bid"' in error_message:
                return Response({'error': 'El monto de la puja debe ser mayor que la puja más alta actual.'}, status=status.HTTP_400_BAD_REQUEST)
            else:
                return Response({'error': 'Error de integridad en la base de datos.'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            # Handle any other unexpected exceptions
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)