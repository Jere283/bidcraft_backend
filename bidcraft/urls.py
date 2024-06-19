from django.urls import path
from rest_framework.urlpatterns import format_suffix_patterns

from .views import create_user, user_detail

urlpatterns = [
    path('user/', create_user, name='create_user'),
    path('user/<int:id>/', user_detail, name='user_detail'),
]

urlpatterns = format_suffix_patterns(urlpatterns)