from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView, get_object_or_404
from .models import Category, Auction, Favorites, User, Tags
from .serializers import CategorySerializer, CreateAuctionSerializer, CreateFavoritesSerializer, GetAuctionSerializer, \
    GetFavoriteSerializer, CreateImageForAuctionSerializer, CreateTagSerializer


class CreateCategoryView(GenericAPIView):
    serializer_class = CategorySerializer

    def get(self, request):
        categories = Category.objects.all()
        serializer = self.serializer_class(categories, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

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

    def delete(self, request, pk):
        try:
            category = Category.objects.get(pk=pk)
            category.delete()
            return Response({
                'message': "Categoría eliminada exitosamente."
            }, status=status.HTTP_204_NO_CONTENT)
        except Category.DoesNotExist:
            return Response({'error': 'Categoría no encontrada'}, status=status.HTTP_404_NOT_FOUND)


class GetAuctionView(GenericAPIView):
    serializer_class = GetAuctionSerializer

    def get(self, request):
        products = Auction.objects.all()
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


class CreateAuctionView(GenericAPIView):
    serializer_class = CreateAuctionSerializer

    def post(self, request):
        product_data = request.data
        serializer = self.serializer_class(data=product_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            product_data = serializer.data
            return Response({
                'data': product_data,
                'message': "La subasta fue creada de manera exitosa"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            product = Auction.objects.get(pk=pk)
            product.delete()
            return Response({
                'message': "La subasta fue borrada de forma correcta"
            }, status=status.HTTP_204_NO_CONTENT)
        except Auction.DoesNotExist:
            return Response({'error': 'Subasta no econtrada'}, status=status.HTTP_404_NOT_FOUND)

    def patch(self, request, pk):
        product = get_object_or_404(Auction, pk=pk)
        serializer = self.serializer_class(instance=product, data=request.data, partial=True)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            return Response(serializer.data, status=status.HTTP_200_OK)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class GetFavoriteView(GenericAPIView):
    serializer_class = GetFavoriteSerializer

    def get(self, request, pk=None):
        try:
            if pk is not None:
                favorites = Favorites.objects.filter(user=pk)
            else:
                favorites = Favorites.objects.all()

            serializer = self.serializer_class(favorites, many=True)
            return Response(serializer.data, status=status.HTTP_200_OK)

        except Favorites.DoesNotExist:
            return Response({"error": "El favorito no fue encontrado"}, status=status.HTTP_404_NOT_FOUND)

        except Exception as e:
            return Response({"error": str(e)}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)


class CreateFavoritesView(GenericAPIView):
    serializer_class = CreateFavoritesSerializer

    def post(self, request):
        favorite_data = request.data
        serializer = self.serializer_class(data=favorite_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            favorite_data = serializer.data
            return Response({
                'data': favorite_data,
                'message': "Favorito creado!"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

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

    def get(self, request, user_id, auction_id):
        favorite_exists = Favorites.objects.filter(user=user_id, auction=auction_id).exists()

        return Response({'exists': favorite_exists}, status=status.HTTP_200_OK)


class DeleteFavoriteUserAuction(GenericAPIView):

    def delete(self, request, user_id, auction_id):
        favorite = Favorites.objects.filter(user=user_id, auction=auction_id)

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


class TagView(GenericAPIView):
    def get(self, request):
        tags = Tags.objects.all()
        serializer = CreateTagSerializer(tags, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        # Obtener el nombre del tag de los datos de la solicitud y capitalizar la primera letra
        tag_name = request.data.get('tag_name', '').capitalize()

        # Verificar si el nombre del tag está presente en los datos de la solicitud
        if not tag_name:
            return Response({'error': 'El nombre del tag es requerido.'}, status=status.HTTP_400_BAD_REQUEST)

        # Verificar si ya existe un tag con las mismas primeras tres letras
        existing_tag = Tags.objects.filter(tag_name__istartswith=tag_name[:3]).first()
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
                'tag_id': tag.tag_id,
                'tag_name': tag.tag_name
            }, status=status.HTTP_201_CREATED)

        # Devolver errores de validación si los datos no son válidos
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            tag = Tags.objects.get(pk=pk)
        except Tags.DoesNotExist:
            return Response({'error': 'Tag no encontrado'}, status=status.HTTP_404_NOT_FOUND)

        tag.delete()
        return Response({'message': 'Tag eliminado exitosamente'}, status=status.HTTP_204_NO_CONTENT)