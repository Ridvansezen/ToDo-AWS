from rest_framework import serializers
from user.models import UserModel
from django.core.validators import MinLengthValidator, MaxLengthValidator
from django.contrib.auth import authenticate
from django.contrib.auth import get_user_model
from django.contrib.auth.hashers import make_password


class UserRegisterSerializer(serializers.ModelSerializer):
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, validators=[MinLengthValidator(limit_value=8), MaxLengthValidator(limit_value=24)])
    password_confirmation = serializers.CharField(write_only=True, style={'input_type': 'password'}, validators=[MinLengthValidator(limit_value=8), MaxLengthValidator(limit_value=24)])

    class Meta:
        model = UserModel
        fields = ('id', 'username','password', 'password_confirmation')
        extra_kwargs = {'password': {'write_only': True}}

    def validate(self, data):
        password = data.get('password')
        password_confirmation = data.get('password_confirmation')

        if password and password_confirmation and password != password_confirmation:
            raise serializers.ValidationError("Password and password confirmation do not match.")

        return data

    def create(self, validated_data):
        user = UserModel.objects.create_user(
            username=validated_data['username'],
            password=validated_data['password'],
        )
        return user
    
    
from django.contrib.auth import authenticate

class UserLoginSerializer(serializers.Serializer):
    username = serializers.CharField()
    password = serializers.CharField(write_only=True, style={'input_type': 'password'}, validators=[MinLengthValidator(limit_value=8), MaxLengthValidator(limit_value=24)])
    
    USERNAME_FIELD = "username"

    def validate(self, data):
        username = data.get('username')
        password = data.get('password')

        user = authenticate(username=username, password=password)

        if user and user.is_active:
            return data
        else:
            raise serializers.ValidationError("Invalid credentials. Please check your username and password.")

