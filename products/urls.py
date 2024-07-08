from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import CreateCategoryView, CreateAuctionView, FavoritesView

urlpatterns = [
    path('categories/', CreateCategoryView.as_view(), name='category-create'),
    path('products/', CreateAuctionView.as_view(), name='list_products'),
    path('favorites/', FavoritesView.as_view(), name='favorites_products'),
    path('favorites/<int:pk>/', FavoritesView.as_view()),  # URL para PUT y DELETE
]