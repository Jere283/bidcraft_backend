from rest_framework_simplejwt.views import TokenObtainPairView
from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from .serializers import CustomUserSerializer

@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = CustomUserSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
@csrf_exempt
def login_view(request):
    try:
        dni = request.data['dni']
        password = request.data['password']
    except KeyError:
        return Response({"detail": "DNI and password are required"}, status=status.HTTP_400_BAD_REQUEST)

    # Authenticate using DNI
    user = authenticate(dni=dni, password=password)
    if user:
        # Return token pair
        token_obtain_pair_view = TokenObtainPairView.as_view()
        return token_obtain_pair_view(request._request)
    return Response({"detail": "Invalid credentials"}, status=status.HTTP_401_UNAUTHORIZED)