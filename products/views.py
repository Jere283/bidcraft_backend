# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import Category, Product, Favorites
from .serializers import CategorySerializer, ProductSerializer, FavoritesSerializer


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
                'message': "Category successfully created."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class CreateProductView(GenericAPIView):
    serializer_class = ProductSerializer
    def get(self, request):
        products = Product.objects.all()
        serializer = self.serializer_class(products, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)
    def post(self, request):
        product_data = request.data
        serializer = self.serializer_class(data=product_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            product_data = serializer.data
            return Response({
                'data': product_data,
                'message': "Product successfully created."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class FavoritesView(GenericAPIView):
    serializer_class = FavoritesSerializer

    def get(self, request):
        favorites = Favorites.objects.all()
        serializer = self.serializer_class(favorites, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

    def post(self, request):
        favorite_data = request.data
        serializer = self.serializer_class(data=favorite_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            favorite_data = serializer.data
            return Response({
                'data': favorite_data,
                'message': "Favorite successfully created."
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def delete(self, request, pk):
        try:
            favorite = Favorites.objects.get(pk=pk)
            favorite.delete()
            return Response({
                'message': "Favorite successfully deleted."
            }, status=status.HTTP_204_NO_CONTENT)
        except Favorites.DoesNotExist:
            return Response({'error': 'Favorite not found'}, status=status.HTTP_404_NOT_FOUND)