from django.core.cache import cache
from django.db import transaction, IntegrityError
from django.views.decorators.cache import cache_page
from rest_framework import status
from rest_framework.pagination import PageNumberPagination
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404
from .models import Category, Auction, Favorites, User, Tags, AuctionsTags, AuctionImage
from .serializers import CategorySerializer, CreateAuctionSerializer, CreateFavoritesSerializer, GetAuctionSerializer, \
    GetFavoriteSerializer, CreateImageForAuctionSerializer, CreateTagSerializer, AuctionsTagsSerializer, \
    TagSerializer, AuctionSerializer
from rest_framework.permissions import IsAuthenticated
from bids.models import Bids



class GetCatergoryView(GenericAPIView):
    serializer_class = CategorySerializer
    def get(self, request):
        categories = Category.objects.all()
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateCategoryView(GenericAPIView):
    serializer_class = CategorySerializer

    def post(self, request):
        category_data = request.data
        serializer = self.serializer_class(data=category_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            category_data = serializer.data
            return Response({
                'data': category_data,
                'message': "La categoria fue creada de manera exitosa"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteCategoryView(GenericAPIView):
    serializer_class = CategorySerializer
    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({
                'message': "Categoría eliminada exitosamente."
            }, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({'error': 'Categoría no encontrada'}, status=status.HTTP_404_NOT_FOUND)


class AuctionPagination(PageNumberPagination):
    page_size = 10

class GetAuctionView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = GetAuctionSerializer
    pagination_class = AuctionPagination

    def get(self, request):

        page_number = request.query_params.get('page', 1)
        cache_key = f'all_auctions_page_{page_number}'

        cached_data = cache.get(cache_key)

        if cached_data:
            return Response(cached_data, status=status.HTTP_200_OK)

        queryset = Auction.objects.filter(is_active=True).exclude(seller=request.user).order_by('auction_id')
        paginator = self.pagination_class()
        result_page = paginator.paginate_queryset(queryset, request)
        serializer = self.serializer_class(result_page, many=True)
        response_data = paginator.get_paginated_response(serializer.data).data

        # Cache the response data
        cache.set(cache_key, response_data, timeout=60 * 15)

        return Response(response_data, status=status.HTTP_200_OK)
class DeleteAuctionView(GenericAPIView):
    def delete(self, request, pk):
        try:
            with transaction.atomic():
                auction = get_object_or_404(Auction, pk=pk)
                AuctionsTags.objects.filter(auction=auction).delete()
                Favorites.objects.filter(auction=auction).delete()
                Bids.objects.filter(auction=auction).delete()
                AuctionImage.objects.filter(auction=auction).delete()
                auction.delete()
                cache.clear()
            return Response({'message': "La subasta fue borrada de forma correcta"}, status=status.HTTP_204_NO_CONTENT)
        except Auction.DoesNotExist:
            return Response({'error': 'Subasta no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except IntegrityError:
            return Response({'error': 'Error de integridad al eliminar'}, status=status.HTTP_400_BAD_REQUEST)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_400_BAD_REQUEST)

class CreateAuctionView(GenericAPIView):
    serializer_class = CreateAuctionSerializer

    def post(self, request):
        product_data = request.data
        serializer = self.serializer_class(data=product_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            product_data = serializer.data
            cache.clear()
            return Response({
                'data': product_data,
                'message': "La subasta fue creada de manera exitosa"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class EditAuctionView(GenericAPIView):
    serializer_class = CreateAuctionSerializer
    def patch(self, request, pk):
        product = get_object_or_404(Auction, pk=pk)
        serializer = self.serializer_class(instance=product, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            cache.clear()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetFavoriteView(GenericAPIView):
    serializer_class = GetFavoriteSerializer
    permission_classes = [IsAuthenticated]

    def get(self, request):
        try:
            if request.user:
                favorites = Favorites.objects.filter(user=request.user.id)
            else:
                favorites = Favorites.objects.all()

            serializer = self.serializer_class(favorites, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Favorites.DoesNotExist:
            return Response({"error": "El favorito no fue encontrado"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateFavoritesView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = CreateFavoritesSerializer

    def post(self, request, auction_id):
        auction = get_object_or_404(Auction, pk=auction_id)
        favorite_data = request.data
        serializer = self.serializer_class(
            data=favorite_data,
            context={'request': request, 'auction':auction}
        )
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            favorite_data = serializer.data
            return Response({
                'data': favorite_data,
                'message': "Favorito creado!"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class DeleteFavoriteView(GenericAPIView):
    serializer_class = CreateFavoritesSerializer

    def delete(self, request, pk):
        try:
            favorite = Favorites.objects.get(user=pk)
            favorite.delete()
            return Response({
                'message': "El favorito fue borrado."
            }, status=status.HTTP_204_NO_CONTENT)
        except Favorites.DoesNotExist:
            return Response({'error': 'favorito no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class CheckFavoriteView(GenericAPIView):

    def get(self, request, auction_id):
        favorite_exists = Favorites.objects.filter(user=request.user.id, auction=auction_id).exists()

        return Response({'exists': favorite_exists}, status=status.HTTP_200_OK)


class DeleteFavoriteUserAuction(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, auction_id):
        favorite = Favorites.objects.filter(user=request.user.id, auction=auction_id)

        if favorite.exists():
            favorite.delete()
            return Response({
                'message': "El favorito fue borrado"
            }, status=status.HTTP_204_NO_CONTENT)

        return Response({'error': 'favorito no encontrado'}, status=status.HTTP_404_NOT_FOUND)


class AuctionFavoriteCountView(GenericAPIView):

    def get(self, request, auction_id):
        try:
            auction = Auction.objects.get(pk=auction_id)
            favorite_count = Favorites.objects.filter(auction=auction).count()
            return Response({'auction_id': auction_id, 'favorite_count': favorite_count}, status=status.HTTP_200_OK)

        except Auction.DoesNotExist:
            return Response({'error': 'Subasta no encontrada'}, status=status.HTTP_404_NOT_FOUND)
        except Exception as e:
            return Response({'error': str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class GetSingleAuctionView(GenericAPIView):
    serializer_class = GetAuctionSerializer

    def get(self, request, auction_id):
        auction = get_object_or_404(Auction, pk=auction_id)
        serializer = self.serializer_class(auction)
        return Response(serializer.data, status=status.HTTP_200_OK)


#obtener la subasta por la id de la categoria
class GetAuctionByCategory(GenericAPIView):
    serializer_class = GetAuctionSerializer

    def get(self, request, category_id):
        auctions = Auction.objects.filter(category=category_id)
        serializer = self.serializer_class(auctions, many=True)

        if auctions.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'error': 'La categoria no tiene subastas'}, status=status.HTTP_404_NOT_FOUND)


class CreateImageForAuction(GenericAPIView):
    
    serializer_class = CreateImageForAuctionSerializer

    def post(self, request):
        image_data = request.data
        serializer = self.serializer_class(data=image_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            image_data = serializer.data
            return Response({
                'data': image_data,
                'message': "La imagen fue agregada a la subasta"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetTagView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request):
        tags = Tags.objects.all()
        serializer = CreateTagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

class CreateTagView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request):
        # Obtener el nombre del tag de los datos de la solicitud y capitalizar la primera letra
        tag_name = request.data.get('tag_name', '').lower()

        # Verificar si el nombre del tag está presente en los datos de la solicitud
        if not tag_name:
            return Response({'error': 'El nombre del tag es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si ya existe el tag
        existing_tag = Tags.objects.filter(tag_name=tag_name).first()
        if existing_tag:
            return Response({
                'message': 'El tag ya existe.',
                'tag_id': existing_tag.tag_id,
                'tag_name': existing_tag.tag_name
            }, status=status.HTTP_409_CONFLICT)

        # Crear un nuevo tag si no existe uno con las mismas primeras tres letras
        serializer = CreateTagSerializer(data={'tag_name': tag_name})
        if serializer.is_valid():
            tag = serializer.save()
            return Response({
                'message': 'Tag creado exitosamente',
                'tag_id': tag.tag_id,
                'tag_name': tag.tag_name
            }, status=status.HTTP_201_CREATED)

        # Devolver errores de validación si los datos no son válidos
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteTagsView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def delete(self, request, pk):
        try:
            tag = Tags.objects.get(pk=pk)
        except Tags.DoesNotExist:
            return Response({'error': 'Tag no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        tag.delete()
        return Response({'message': 'Tag eliminado exitosamente'}, status=status.HTTP_204_NO_CONTENT)

class FindTagsView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, tag_name):
        # Tomar las primeras tres letras del tag_name y convertir a minúsculas
        prefix = tag_name[:3].lower()

        # Buscar todos los tags que empiecen con esas tres letras
        matching_tags = Tags.objects.filter(tag_name__istartswith=prefix)
        serializer = CreateTagSerializer(matching_tags, many=True)

        return Response(serializer.data, status=status.HTTP_200_OK)

class GetAuctionsByUser(GenericAPIView):

    serializer_class = GetAuctionSerializer
    permission_classes = [IsAuthenticated]
    def get(self, request):
        user = request.user
        auctions = Auction.objects.filter(seller=user)
        serializer = self.serializer_class(auctions, many=True)

        if auctions.exists():
            return Response(serializer.data, status=status.HTTP_200_OK)

        return Response({'error': 'El usuario no tiene subastas'}, status=status.HTTP_404_NOT_FOUND)


class CreateAuctionTagView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def post(self, request, auction_id):
        # Obtener el nombre del tag de los datos de la solicitud y convertir a minúsculas
        tag_name = request.data.get('tag_name', '').lower()

        # Verificar si el nombre del tag está presente en los datos de la solicitud
        if not tag_name:
            return Response({'error': 'El nombre del tag es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si ya existe el tag
        existing_tag = Tags.objects.filter(tag_name=tag_name).first()
        if existing_tag:
            auction = get_object_or_404(Auction, pk=auction_id)

            # Crear la relación AuctionsTags
            auction_tag_serializer = AuctionsTagsSerializer(data={'tag': existing_tag.tag_id, 'auction': auction.auction_id})
            if auction_tag_serializer.is_valid():
                auction_tag_serializer.save()
                return Response({
                    'message': 'Tag relacionado con la subasta',
                    'auction_tag': auction_tag_serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(auction_tag_serializer.errors, status=status.HTTP_400_BAD_REQUEST)

        # Crear un nuevo tag si no existe uno con el mismo nombre exacto
        tag_serializer = CreateTagSerializer(data={'tag_name': tag_name})
        if tag_serializer.is_valid():
            tag = tag_serializer.save()
            auction = get_object_or_404(Auction, pk=auction_id)

            # Crear la relación AuctionsTags
            auction_tag_serializer = AuctionsTagsSerializer(data={'tag': tag.tag_id, 'auction': auction.auction_id})
            if auction_tag_serializer.is_valid():
                auction_tag_serializer.save()
                return Response({
                    'message': 'Tag creado exitosamente y relacionado con la subasta',
                    'auction_tag': auction_tag_serializer.data
                }, status=status.HTTP_201_CREATED)
            else:
                return Response(auction_tag_serializer.errors, status=status.HTTP_400_BAD_REQUEST)
        else:
            return Response(tag_serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class TagsByAuctionView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, auction_id):
        auction = get_object_or_404(Auction, pk=auction_id)
        auction_tags = AuctionsTags.objects.filter(auction=auction)
        tags = [at.tag for at in auction_tags]
        serializer = TagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

# Vista para obtener todas las subastas asociadas a un tag
class AuctionsByTagView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, tag_id):
        tag = get_object_or_404(Tags, pk=tag_id)
        auction_tags = AuctionsTags.objects.filter(tag=tag)
        auctions = [at.auction for at in auction_tags]
        serializer = AuctionSerializer(auctions, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class GetAllAuctionsbyTag(GenericAPIView):
    permission_classes = [IsAuthenticated]
    def get(self, request, tag_name):
        # Tomar las primeras tres letras del tag_name y convertir a minúsculas
        prefix = tag_name[:3].lower()

        # Buscar todos los tags que empiecen con esas tres letras
        matching_tags = Tags.objects.filter(tag_name__istartswith=prefix)
        tags = CreateTagSerializer(matching_tags, many=True)
        auctions_res = []
        for tag in tags.data:

            auction_tags = AuctionsTags.objects.filter(tag=tag['tag_id'])
            auctions = [at.auction for at in auction_tags]
            serializer = GetAuctionSerializer(auctions, many=True)
            if len(serializer.data) > 0:
                auctions_res.append(serializer.data)

        return Response(auctions_res, status=status.HTTP_200_OK)