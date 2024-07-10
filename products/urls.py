from rest_framework.routers import DefaultRouter
from django.urls import path, include

from .views import CreateCategoryView, CreateAuctionView, CreateFavoritesView, GetAuctionView, GetFavoriteView

urlpatterns = [
    #CATEGORIAS
    path('categories/show/all/', CreateCategoryView.as_view(), name='show_category'),
    path('categories/create/one/', CreateCategoryView.as_view(), name='create_category'),
    path('categories/delete/one/<int:pk>/', CreateCategoryView.as_view(), name='delete_category'),  # URL para DELETE
    #SUBASTAS
    path('auction/show/all/', GetAuctionView.as_view(), name='show_products'),
    path('auction/create/one/', CreateAuctionView.as_view(), name='create_products'),
    path('auction/edit/one/<int:pk>/', CreateAuctionView.as_view(), name='edit_products'),
    path('auction/delete/one/<int:pk>/', CreateAuctionView.as_view(), name='delete_products'),  # URL para PUT y DELETE
    #FAVORITOS
    path('favorites/show/all/', GetFavoriteView.as_view(), name='show_favorites_products'),
    path('favorites/create/one/', CreateFavoritesView.as_view(), name='create_favorites_product'),
    path('favorites/delete/one/<int:pk>/', CreateFavoritesView.as_view(), name='delete_favorites_products'),
    path('favorites/user/<str:pk>/', GetFavoriteView.as_view(), name='favorites_byUser_products'),
]