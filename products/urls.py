from django.urls import path, include

from .views import CreateCategoryView, CreateAuctionView, CreateFavoritesView, GetAuctionView, GetFavoriteView, \
    CheckFavoriteView, AuctionFavoriteCountView, GetSingleAuctionView, DeleteFavoriteUserAuction, GetAuctionByCategory, \
    CreateImageForAuction, TagView

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
    path('auction/show/all/category/<int:category_id>/', GetAuctionByCategory.as_view(), name='show_products_by_category'),
    path('auction/favorite/count/<int:auction_id>/', AuctionFavoriteCountView.as_view(), name='auction-favorite-count'),
    path('auction/show/one/<int:auction_id>/', GetSingleAuctionView.as_view(), name='get-single-auction'),
    path('auction/image/add', CreateImageForAuction.as_view(), name='add-image-auction'),
    #TAGS
    path('tags/show/all/', TagView.as_view(), name='show_tags'),
    path('tags/create/one/', TagView.as_view(), name='create_tags'),
    path('tags/edit/one/<int:pk>/', TagView.as_view(), name='edit_tags'),
    path('tags/delete/one/<int:pk>/', TagView.as_view(), name='delete_tags'),
    #FAVORITOS
    path('favorites/show/all/', GetFavoriteView.as_view(), name='show_favorites_products'),
    path('favorites/create/one/', CreateFavoritesView.as_view(), name='create_favorites_product'),
    path('favorites/delete/one/<int:pk>/', CreateFavoritesView.as_view(), name='delete_favorites_products'),
    path('favorites/user/<str:pk>/', GetFavoriteView.as_view(), name='favorites_byUser_products'),
    path('favorites/<str:user_id>/<int:auction_id>/', CheckFavoriteView.as_view(), name='check-favorite'),
    path('favorites/delete/one/<str:user_id>/<int:auction_id>/',DeleteFavoriteUserAuction.as_view(), name='check-del-favorite'),
]