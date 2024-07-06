from django import forms
from django.contrib.auth.forms import UserCreationForm, UserChangeForm
from .models import User

class CustomUserCreationForm(UserCreationForm):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'second_name', 'last_name', 'last_name2', 'phone_number')

class CustomUserChangeForm(UserChangeForm):
    class Meta:
        model = User
        fields = ('id', 'email', 'username', 'first_name', 'second_name', 'last_name', 'last_name2', 'phone_number')
