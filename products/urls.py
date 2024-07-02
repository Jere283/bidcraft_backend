#from rest_framework import routers
#from .api import CategoryViewSet, ProductViewSet

#router = routers.DefaultRouter()
#routers.register('api/category/', CategoryViewSet, 'category')
#routers.register('api/product/', ProductViewSet, 'product')

#urlpatterns = router.urls

from rest_framework.routers import DefaultRouter
from .api import CategoryViewSet, ProductViewSet
from django.urls import path, include

router = DefaultRouter()
router.register('category/', CategoryViewSet, basename='category')
router.register('product/', ProductViewSet, basename='product')

urlpatterns = [
    path('', include(router.urls)),
]
