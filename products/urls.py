from rest_framework.routers import DefaultRouter
from .api import CategoryViewSet, ProductViewSet
from django.urls import path, include

from .views import CreateCategoryView

urlpatterns = [
    path('categories/', CreateCategoryView.as_view(), name='category-create'),
]