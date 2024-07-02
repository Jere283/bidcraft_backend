#from rest_framework import routers
#from .api import CategoryViewSet, ProductViewSet

#router = routers.DefaultRouter()
#routers.register('api/category/', CategoryViewSet, 'category')
#routers.register('api/product/', ProductViewSet, 'product')

#urlpatterns = router.urls

from rest_framework.routers import DefaultRouter
from .api import CategoryViewSet, ProductViewSet
from django.urls import path, include

from .views import CreateCategoryView, CreateProductView, FavoritesView

urlpatterns = [
    path('categories/', CreateCategoryView.as_view(), name='category-create'),
    path('products/', CreateProductView.as_view(), name='list_products'),
    path('favorites/', FavoritesView.as_view(), name='favorites_products'),
]