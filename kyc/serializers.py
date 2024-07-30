from rest_framework import serializers
from rest_framework.generics import DestroyAPIView

from users.serializers import UserRegisterSerializer
from .models import KycStatus, UsersKyc
from products.models import Auction
from users.models import User
from django.utils import timezone

class KycStatusSerializer(serializers.ModelSerializer):
    class Meta:
        model = KycStatus
        fields = ['status_id', 'status']


class UsersKycSerializer(serializers.ModelSerializer):

    user = UserRegisterSerializer(read_only=True)
    status = KycStatusSerializer(read_only=True)
    class Meta:
        model = UsersKyc
        fields = ['user', 'front_id', 'back_id', 'profile_picture', 'status', 'comment']

    def create(self, validated_data):
        request = self.context.get('request')
        user = request.user
        status_revision = KycStatus.objects.get(status_id=1)

        users_kyc = UsersKyc.objects.create(
            user=user,
            front_id=validated_data.get('front_id', ''),
            back_id=validated_data.get('back_id', ''),
            profile_picture=validated_data.get('profile_picture', ''),
            status=status_revision,
            comment=validated_data.get('comment', '')
        )
        return users_kyc
