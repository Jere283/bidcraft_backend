from rest_framework.permissions import AllowAny
from rest_framework.decorators import api_view, permission_classes
from rest_framework.response import Response
from rest_framework import status
from django.contrib.auth import authenticate
from rest_framework.generics import GenericAPIView

from .models import Otps
from .serializers import UserRegisterSerializer
from .utils import send_generated_otp_to_email


class RegisterUserView(GenericAPIView):
    serializer_class = UserRegisterSerializer

    def post(self, request):
        user_data=request.data
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
                "message" : "El usuario ya fue verificado"
            },status.HTTP_204_NO_CONTENT)
        except Otps.DoesNotExist as identifier:
            return Response({
                'message': "El codigo no existe"
            }, status.HTTP_404_NOT_FOUND)
