# views.py
from rest_framework import status
from rest_framework.response import Response
from rest_framework.generics import GenericAPIView
from .models import Category
from .serializers import CategorySerializer

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