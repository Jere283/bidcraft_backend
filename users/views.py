
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView
from rest_framework.permissions import IsAuthenticated
from .models import Otps
from .serializers import UserRegisterSerializer, LoginSerializer
from .utils import send_generated_otp_to_email


class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data = request.data
        serializer = self.serializer_class(data=user_data)
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            user_data = serializer.data
            send_generated_otp_to_email(user_data['email'], request)
            return Response({
                'data': user_data,
                'message': f"Gracias por registrate, un codigo de verificacion fue enviado a tu correo"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class VerifyUserEmail(GenericAPIView):
    def post(self, request):
        otp_code = request.data.get('otp')
        try:
            user_code_obj = Otps.objects.get(code=otp_code)
            user = user_code_obj.user
            if not user.otp_verified:
                user.otp_verified = True
                user.save()
                return Response(
                    {
                        'message': "El correo fue verificado de manera exitosa"
                    }, status=status.HTTP_200_OK)
            return Response({
                "message": "El usuario ya fue verificado"
            }, status.HTTP_204_NO_CONTENT)
        except Otps.DoesNotExist as identifier:
            return Response({
                'message': "El codigo no existe"
            }, status.HTTP_404_NOT_FOUND)


class LoginUserView(GenericAPIView):
    serializer_class = LoginSerializer

    def post(self, request):
        serializer = self.serializer_class(data=request.data, context={'request': request})
        serializer.is_valid(raise_exception=True)

        return Response(serializer.data, status=status.HTTP_200_OK)


class profile(GenericAPIView):
    permission_classes = [IsAuthenticated]

    def get(self, request):
        user = request.user  # Get the authenticated user
        data = {
            'id': user.id,
            'email': user.email,
            'username': user.email,
            'first_name': user.first_name,
            'last_name': user.last_name,
            'profile_img': user.profile_img
        }
        return Response(data, status=status.HTTP_200_OK)




