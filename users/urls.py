from django.urls import path
from .views import RegisterUserView, VerifyUserEmail, LoginUserView, profile

urlpatterns = [
    path('register/', RegisterUserView.as_view(), name='register'),
    path('verify_email/', VerifyUserEmail.as_view(), name='verify'),
    path('login/', LoginUserView.as_view(), name='login'),
    path('profile/', profile.as_view(), name='granted'),
]
