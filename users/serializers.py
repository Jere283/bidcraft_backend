from rest_framework import serializers
from .models import users
from django.contrib.auth import get_user_model

class CustomUserSerializer(serializers.ModelSerializer):
    class Meta:
        model = users
        fields = ('dni', 'email', 'username', 'first_name', 'second_name', 'last_name', 'last_name2', 'phone_number', 'password')
        extra_kwargs = {'password': {'write_only': True}}

    def create(self, validated_data):
        user = users.objects.create_user(
            dni=validated_data['dni'],
            email=validated_data['email'],
            username=validated_data['username'],
            password=validated_data['password'],
            first_name=validated_data['first_name'],
            second_name=validated_data.get('second_name', ''),
            last_name=validated_data['last_name'],
            last_name2=validated_data.get('last_name2', ''),
            phone_number=validated_data.get('phone_number', '')
        )
        return user
