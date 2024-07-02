from rest_framework import serializers
from .models import User, Addresses
from django.contrib.auth import get_user_model

class UserRegisterSerializer(serializers.ModelSerializer):

    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    password_confirm = serializers.CharField(max_length=68, min_length=8, write_only=True)
    class Meta:
        model = User
        fields = ('user_id', 'email', 'username', 'first_name', 'second_name', 'last_name', 'last_name2', 'phone_number'
                  , 'password', 'password_confirm', 'address_id')

    def validate(self, attrs):
        password = attrs.get('password', '')
        password_confirm = attrs.get('password_confirm', '')

        if password != password_confirm:
            raise serializers.ValidationError("Las contaseñas no coinciden.")
        return attrs
    def create(self, validated_data):

        user = User.objects.create_user(
            user_id=validated_data['user_id'],
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            second_name=validated_data.get('second_name', ''),
            last_name=validated_data['last_name'],
            last_name2=validated_data.get('last_name2', ''),
            phone_number=validated_data.get('phone_number', ''),
            address=validated_data.get('address_id', None),
        )
        return user


class LoginSerializer(serializers.ModelSerializer):
    pass