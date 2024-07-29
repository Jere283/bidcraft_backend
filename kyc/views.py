from django.shortcuts import render
from rest_framework.exceptions import NotFound, PermissionDenied

# Create your views here.
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.generics import GenericAPIView, ListAPIView, DestroyAPIView, UpdateAPIView

import users
from .serializers import UsersKycSerializer, KycStatusSerializer
from .models import UsersKyc, KycStatus
from django.shortcuts import get_object_or_404
from django.db import IntegrityError
from rest_framework.permissions import IsAuthenticated

#OBTENER TODOS LOS ESTADOS QUE PUEDE TENER UNA VERIFICACION DE DNI
class KycStatusListView(APIView):
    def get(self, request):
        statuses = KycStatus.objects.all()
        serializer = KycStatusSerializer(statuses, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)


#OBTENER POR STATUS_ID En que estado se encuentra unaDE DNI
class UsersKycByStatusView(ListAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsersKycSerializer

    def get_queryset(self):
        status_id = self.kwargs.get('status_id')
        return UsersKyc.objects.filter(status_id=status_id)

class CreateUsersKycView(GenericAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsersKycSerializer

    def post(self, request):
        kyc_data = request.data

        # Asignar el status_id=1 para el nuevo KYC
        try:
            status_revision = KycStatus.objects.get(status_id=1)
        except KycStatus.DoesNotExist:
            return Response({'error': 'El estado de revisión no existe.'}, status=status.HTTP_400_BAD_REQUEST)

        kyc_data['status'] = status_revision.status_id

        serializer = self.serializer_class(
            data=kyc_data,
            context={'request': request})
        if serializer.is_valid(raise_exception=True):
            serializer.save()
            kyc_data = serializer.data
            return Response({
                'data': kyc_data,
                'message': "KYC creado exitosamente"
            }, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

class DeleteUsersKycView(DestroyAPIView):
    permission_classes = [IsAuthenticated]

    def delete(self, request, user_id, *args, **kwargs):
        user_kyc = get_object_or_404(UsersKyc, user_id=user_id)
        user_kyc.delete()
        return Response({
            'message': 'Users KYC eliminado correctamente'
        }, status=status.HTTP_204_NO_CONTENT)

#Vista para editar front_id, back_id, profile_picture y comment
class UpdateUsersKycView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsersKycSerializer

    def get_object(self):
        # Obtén el ID de usuario de los parámetros de la URL
        user_id = self.kwargs.get('user_id')
        try:
            # Busca el objeto UsersKyc asociado con el ID de usuario
            user_kyc = UsersKyc.objects.get(user__id=user_id)
        except UsersKyc.DoesNotExist:
            # Lanza una excepción si el objeto no existe
            raise NotFound(detail="No UsersKyc matches the given query.")
        return user_kyc

    def patch(self, request, *args, **kwargs):
        user_kyc = self.get_object()
        partial_data = {
            'front_id': request.data.get('front_id', user_kyc.front_id),
            'back_id': request.data.get('back_id', user_kyc.back_id),
            'profile_picture': request.data.get('profile_picture', user_kyc.profile_picture),
            'comment': request.data.get('comment', user_kyc.comment),
        }
        serializer = self.serializer_class(user_kyc, data=partial_data, partial=True)
        if serializer.is_valid():
            serializer.save()
            return Response(serializer.data)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

#Vista para editar status solo si el usuario es is_staff y is_superuser
class UpdateUsersKycStatusView(UpdateAPIView):
    permission_classes = [IsAuthenticated]
    serializer_class = UsersKycSerializer
    queryset = UsersKyc.objects.all()

    def patch(self, request, user_id, *args, **kwargs):
        # Verifica permisos
        if not request.user.is_staff or not request.user.is_superuser:
            raise PermissionDenied('No tienes permiso para realizar esta acción.')

        # Busca el objeto UsersKyc
        user_kyc = get_object_or_404(UsersKyc, user__id=user_id)

        # Obtén el estado del JSON
        status_id = request.data.get('status')

        # Verifica si el estado existe
        try:
            new_status = KycStatus.objects.get(status_id=status_id)
        except KycStatus.DoesNotExist:
            return Response({'error': 'El estado proporcionado no existe.'}, status=status.HTTP_400_BAD_REQUEST)

        # Actualiza el estado
        user_kyc.status = new_status
        user_kyc.save()

        # Devuelve los datos actualizados
        serializer = self.serializer_class(user_kyc)
        return Response(serializer.data)
