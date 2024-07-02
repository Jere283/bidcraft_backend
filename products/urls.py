#from rest_framework import routers
#from .api import CategoryViewSet, ProductViewSet

#router = routers.DefaultRouter()
#routers.register('api/category/', CategoryViewSet, 'category')
#routers.register('api/product/', ProductViewSet, 'product')

#urlpatterns = router.urls

from rest_framework.routers import DefaultRouter
from .api import CategoryViewSet, ProductViewSet
from django.urls import path, include

from .views import CreateCategoryView

urlpatterns = [
    path('categories/', CreateCategoryView.as_view(), name='category-create'),
]