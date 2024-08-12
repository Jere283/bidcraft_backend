from datetime import timezone

from django.db import IntegrityError
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404, ListAPIView
from rest_framework.views import APIView
from django.core.cache import cache

from products.models import Auction
from users.serializers import UserRegisterSerializer
from .models import CompletedAuctions, SellerReviews, Bids, Notifications, Purchases
from .serializers import CreateBidSerializer, CompletedAuctionSerializer, SellerReviewsSerializer, GetBidSerializer, \
    GetNotificationsSerializer, PurchasesSerializer
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

    def get(self, request, *args, **kwargs):
        user = request.user

        # Filtrar las reseñas realizadas por el usuario logueado
        reviews = SellerReviews.objects.filter(buyer=user)

        # Si existen reseñas, serializarlas y añadir la información del comprador y del vendedor
        if reviews.exists():
            review_data_list = []
            for review in reviews:
                review_serializer = SellerReviewsSerializer(review)
                review_data = review_serializer.data

                # Obtener y serializar los datos del vendedor
                seller = User.objects.get(id=review_data['seller'])
                seller_serializer = UserRegisterSerializer(seller)
                review_data['seller'] = seller_serializer.data

                # Obtener y serializar los datos del comprador (usuario logueado)
                buyer_serializer = UserRegisterSerializer(user)
                review_data['buyer'] = buyer_serializer.data

                review_data_list.append(review_data)

            return Response({
                'message': 'Reseñas obtenidas satisfactoriamente.',
                'data': review_data_list
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'No existen reseñas realizadas por el usuario.',
                'buyer': UserRegisterSerializer(user).data
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

        # Enviar un mensaje de confirmación
        return Response({'message': 'Reseña eliminada satisfactoriamente'}, status=status.HTTP_200_OK)


class SellerReviewsBySellerView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, seller_id, *args, **kwargs):
        # Verificar si el vendedor existe
        try:
            seller = User.objects.get(id=seller_id)
        except User.DoesNotExist:
            return Response({'error': 'El vendedor no existe.'}, status=status.HTTP_404_NOT_FOUND)

        # Obtener todas las reseñas para este vendedor
        reviews = SellerReviews.objects.filter(seller=seller)

        # Serializar los datos del vendedor
        seller_serializer = UserRegisterSerializer(seller)

        # Si existen reseñas, serializarlas y añadir la información del vendedor
        if reviews.exists():
            review_serializer = SellerReviewsSerializer(reviews, many=True)
            review_data = review_serializer.data
            for review in review_data:
                review['seller'] = seller_serializer.data
                # Serializar los datos del comprador
                buyer = User.objects.get(id=review['buyer'])
                buyer_serializer = UserRegisterSerializer(buyer)
                review['buyer'] = buyer_serializer.data

            return Response({
                'message': 'Reseñas obtenidas satisfactoriamente.',
                'data': review_data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'No existen reseñas para este vendedor.',
                'seller': seller_serializer.data
            }, status=status.HTTP_200_OK)


class SellerReviewByAuctionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, auction_id, *args, **kwargs):
        # Verificar si la subasta existe
        try:
            auction = Auction.objects.get(auction_id=auction_id)
        except Auction.DoesNotExist:
            return Response({'error': 'La subasta no existe.'}, status=status.HTTP_404_NOT_FOUND)

        # Obtener la reseña asociada con la subasta
        try:
            review = SellerReviews.objects.get(auction=auction)
        except SellerReviews.DoesNotExist:
            review = None

        # Obtener la información del vendedor
        seller = auction.seller

        # Serializar los datos del vendedor
        seller_serializer = UserRegisterSerializer(seller)

        # Si existe una reseña, serializarla y añadir la información del vendedor
        if review:
            review_serializer = SellerReviewsSerializer(review)
            review_data = review_serializer.data
            review_data['seller'] = seller_serializer.data
            return Response({
                'message': 'Reseña obtenida.',
                'data': review_data
            }, status=status.HTTP_200_OK)
        else:
            return Response({
                'message': 'No existe una reseña para esta subasta.',
                'seller': seller_serializer.data
            }, status=status.HTTP_200_OK)

class ShowBidsByAuctionID(GenericAPIView):
    serializer_class = GetBidSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request, auction_id):

       bids = Bids.objects.filter(auction = auction_id)
       serializer = self.serializer_class(bids, many=True)

       return Response(data={'data':serializer.data}, status=status.HTTP_200_OK)


class ShowNotifications(GenericAPIView):
    serializer_class = GetNotificationsSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        is_read_param = request.query_params.get('is_read', None)

        if is_read_param is not None:
            is_read = is_read_param.lower() == 'true'
            notifications = Notifications.objects.filter(user=request.user, is_read=is_read)
        else:
            notifications = Notifications.objects.filter(user=request.user)

        if not notifications.exists():
            return Response(data={'message': "No hay notificaciones"}, status=status.HTTP_200_OK)

        serializer = self.serializer_class(notifications, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class MarkNotificationAsRead(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def post(self, request, notification_id):
        try:
            notification = Notifications.objects.get(notification_id=notification_id)
        except Notifications.DoesNotExist:
            return Response(data={'error': "La notificación no existe"}, status=status.HTTP_404_NOT_FOUND)

        if notification.user == request.user:
            notification.is_read = True
            notification.save()
            return Response(data={'data': "Has leido la notificaion"}, status=status.HTTP_200_OK)
        else:
            return Response(data={'error': "La notificacion no te pertenece"}, status=status.HTTP_400_BAD_REQUEST)


class AllPurchasesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        purchases = Purchases.objects.all()
        serializer = PurchasesSerializer(purchases, many=True)
        return Response({
            'message': 'Facturas obtenidas satisfactoriamente',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class UserPurchasesView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, *args, **kwargs):
        user = request.user
        purchases = Purchases.objects.filter(buyer=user)
        serializer = PurchasesSerializer(purchases, many=True)
        return Response({
            'message': 'Facturas del usuario obtenidas satisfactoriamente',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

class PurchasesByAuctionView(APIView):
    permission_classes = [IsAuthenticated]

    def get(self, request, auction_id, *args, **kwargs):
        purchases = Purchases.objects.filter(auction_id=auction_id)
        if not purchases.exists():
            return Response({'error': 'No existen facturas para esta subasta.'}, status=status.HTTP_404_NOT_FOUND)

        serializer = PurchasesSerializer(purchases, many=True)
        return Response({
            'message': 'Facturas obtenidas para la subasta.',
            'data': serializer.data
        }, status=status.HTTP_200_OK)

