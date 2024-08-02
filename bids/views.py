from datetime import timezone

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404, ListAPIView
from rest_framework.views import APIView
from django.core.cache import cache

from products.models import Auction
from .models import CompletedAuctions, SellerReviews
from .serializers import CreateBidSerializer, CompletedAuctionSerializer, SellerReviewsSerializer
from rest_framework.permissions import IsAuthenticated
from django.utils import timezone
from django.contrib.auth.models import User
from users.models import User


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
                cache.clear()
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


class UserCompletedAuctionsView(GenericAPIView):
    serializer_class = CompletedAuctionSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user
        win_auctions = CompletedAuctions.objects.filter(buyer=user)
        serializer = self.serializer_class(win_auctions, many=True)

        if win_auctions.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'message': 'El usuario no tiene subastas ganadas'}, status=status.HTTP_200_OK)


class CreateSellerReviewView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerReviewsSerializer

    def post(self, request, auction_id, *args, **kwargs):
        buyer = request.user

        # Verificar si la subasta y el comprador existen en CompletedAuctions
        try:
            completed_auction = CompletedAuctions.objects.get(auction_id=auction_id, buyer=buyer)
        except CompletedAuctions.DoesNotExist:
            return Response({'error': 'No existe la compra para realizar un comentario y calificación.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Verificar si ya existe una reseña para esta subasta por este comprador
        if SellerReviews.objects.filter(auction_id=auction_id, buyer=buyer).exists():
            return Response({'error': 'Ya has realizado una reseña para esta subasta.'},
                            status=status.HTTP_400_BAD_REQUEST)

        # Obtener el objeto de la subasta y asegurar que el campo 'seller' sea el correcto
        try:
            auction = Auction.objects.get(auction_id=auction_id)
            seller_id = auction.seller.id
        except Auction.DoesNotExist:
            return Response({'error': 'La subasta no existe.'}, status=status.HTTP_400_BAD_REQUEST)

        # Crear la data para el serializer
        review_data = {
            'seller': seller_id,
            'auction': auction_id,
            'rating': request.data.get('rating'),
            'comment': request.data.get('comment'),
        }

        serializer = self.serializer_class(data=review_data)

        if serializer.is_valid():
            # Asignar el comprador (buyer) y la fecha actual antes de guardar
            review = serializer.save(buyer=buyer, review_date=timezone.now())
            return Response({
                'message': 'Review creada satisfactoriamente',
                'data': SellerReviewsSerializer(review).data
            }, status=status.HTTP_201_CREATED)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class SellerReviewListView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerReviewsSerializer

    def get(self, request, *args, **kwargs):
        user = request.user

        # Filtrar las reseñas realizadas por el usuario logueado
        reviews = SellerReviews.objects.filter(buyer=user)

        # Serializar los datos
        serializer = self.serializer_class(reviews, many=True)

        return Response({
            'message': 'Reseñas obtenidas satisfactoriamente',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class SellerReviewByAuctionView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerReviewsSerializer

    def get(self, request, auction_id, *args, **kwargs):
        # Verificar si la subasta existe
        try:
            auction = Auction.objects.get(auction_id=auction_id)
        except Auction.DoesNotExist:
            return Response({'error': 'La subasta no existe.'}, status=status.HTTP_404_NOT_FOUND)

        # Obtener las reseñas asociadas con la subasta
        reviews = SellerReviews.objects.filter(auction=auction)

        # Serializar los datos
        serializer = self.serializer_class(reviews, many=True)

        return Response({
            'message': 'Reseñas obtenidas.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)


class UpdateSellerReviewView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerReviewsSerializer
    def patch(self, request, auction_id, *args, **kwargs):
        user = request.user

        # Verificar si la subasta existe
        try:
            auction = Auction.objects.get(auction_id=auction_id)
        except Auction.DoesNotExist:
            return Response({'error': 'La subasta no existe.'}, status=status.HTTP_404_NOT_FOUND)

        # Obtener la reseña del usuario para esta subasta
        try:
            review = SellerReviews.objects.get(auction=auction, buyer=user)
        except SellerReviews.DoesNotExist:
            return Response({'error': 'No tienes una reseña para esta subasta o no hiciste la compra.'},
                            status=status.HTTP_404_NOT_FOUND)

        # Serializar los datos recibidos y permitir solo los campos `comment` y `rating`
        serializer = SellerReviewsSerializer(review, data=request.data, partial=True)

        if serializer.is_valid():
            serializer.save()
            return Response({
                'message': 'Reseña actualizada',
                'data': serializer.data
            }, status=status.HTTP_200_OK)

        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteSellerReviewView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerReviewsSerializer
    def delete(self, request, auction_id, *args, **kwargs):
        user = request.user

        # Verificar si la subasta existe
        try:
            auction = Auction.objects.get(auction_id=auction_id)
        except Auction.DoesNotExist:
            return Response({'error': 'La subasta no existe.'}, status=status.HTTP_404_NOT_FOUND)

        # Obtener la reseña del usuario para esta subasta
        try:
            review = SellerReviews.objects.get(auction=auction, buyer=user)
        except SellerReviews.DoesNotExist:
            return Response({'error': 'No tienes una reseña para esta subasta o la reseña no existe.'},
                            status=status.HTTP_404_NOT_FOUND)

        # Eliminar la reseña
        review.delete()

        return Response({'message': 'Reseña eliminada satisfactoriamente'}, status=status.HTTP_204_NO_CONTENT)


class SellerReviewsBySellerView(APIView):
    permission_classes = [IsAuthenticated]
    serializer_class = SellerReviewsSerializer

    def get(self, request, seller_id, *args, **kwargs):
        # Verificar si el vendedor existe
        try:
            seller = User.objects.get(id=seller_id)
        except User.DoesNotExist:
            return Response({'error': 'El vendedor no existe.'}, status=status.HTTP_404_NOT_FOUND)

        # Obtener todas las reseñas para este vendedor
        reviews = SellerReviews.objects.filter(seller=seller)

        # Serializar los datos
        serializer = self.serializer_class(reviews, many=True)

        return Response({
            'message': 'Reseñas obtenidas satisfactoriamente',
            'data': serializer.data
        }, status=status.HTTP_200_OK)