from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView
from .serializers import UserRegisterSerializer
from .utils import send_code_to_user


@api_view(['POST'])
@permission_classes([AllowAny])
def register_view(request):
    serializer = UserRegisterSerializer(data=request.data)
    if serializer.is_valid():
        serializer.save()
        return Response(serializer.data, status=status.HTTP_201_CREATED)
    return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data=request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user = serializer.data
            ##send_code_to_user(user['email'])
            return Response({
                'data': user,
                'message': f"Gracias por registrate, un codigo de verificacion fue enviado a tu correo"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


@api_view(['POST'])
@permission_classes([AllowAny])
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