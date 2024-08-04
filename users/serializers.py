from rest_framework import serializers
from rest_framework.exceptions import AuthenticationFailed

from .models import User, Addresses
from django.contrib.auth import get_user_model, authenticate


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(max_length=68, min_length=8, write_only=True)
    password_confirm = serializers.CharField(max_length=68, min_length=8, write_only=True)

    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'second_name', 'last_name', 'last_name2', 'phone_number'
                  , 'password', 'password_confirm', 'address_id')

    def validate(self, attrs):
        password = attrs.get('password', '')
        password_confirm = attrs.get('password_confirm', '')

        if password != password_confirm:
            raise serializers.ValidationError("Las contaseñas no coinciden.")


        id = User.objects.filter(id=attrs.get('id')).exists()
        email = User.objects.filter(email=attrs.get('email')).exists()
        username = User.objects.filter(username=attrs.get('username')).exists()

        return attrs

    def create(self, validated_data):
        user = User.objects.create_user(
            id=validated_data['id'],
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
    email = serializers.EmailField(max_length=255, min_length=6)
    password = serializers.CharField(max_length=68, write_only=True)
    id = serializers.CharField(read_only=True)
    full_name = serializers.CharField(max_length=255, read_only=True)
    access_token = serializers.CharField(max_length=255, read_only=True)
    refresh_token = serializers.CharField(max_length=255, read_only=True)

    class Meta:
        model = User
        fields = ['email', 'id', 'password', 'full_name', 'access_token', 'refresh_token']

    def validate(self, attrs):
        email = attrs.get('email')
        password = attrs.get('password')
        request = self.context.get('request')
        user = authenticate(request, email=email, password=password)
        if not user:
            raise AuthenticationFailed("Las credenciales son invalidas")
        if not user.otp_verified:
            raise AuthenticationFailed("El correo no esta verificado")
        user_tokens = user.tokens()

        return {
            'email': user.email,
            'id': user.id,
            'full_name': user.get_full_name,
            'access_token': str(user_tokens.get('access')),
            'refresh_token': str(user_tokens.get('refresh'))
        }
