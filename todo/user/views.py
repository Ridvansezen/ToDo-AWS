from django.shortcuts import render
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status
from rest_framework.permissions import AllowAny
from user.serializers import UserRegisterSerializer
from user.serializers import UserLoginSerializer
from django.contrib.auth import authenticate, login, logout
from django.core.exceptions import ValidationError



class RegisterAPIView(APIView):
    serializer_class = UserRegisterSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            user = serializer.save()
            login(request, user)
            return Response({'message': 'User signed up successfully.'}, status=status.HTTP_201_CREATED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        serializer = self.serializer_class()
        return Response({'serializer': serializer.data})
    
    

class LoginAPIView(APIView):
    serializer_class = UserLoginSerializer

    def post(self, request, *args, **kwargs):
        serializer = self.serializer_class(data=request.data)
        if serializer.is_valid():
            username = serializer.validated_data.get('username')
            password = serializer.validated_data.get('password')

            user = authenticate(username=username, password=password)

            if user:
                login(request, user)
                return Response({"message": "User signed in successfully."}, status=status.HTTP_200_OK)
            else:
                return Response({"error": "Invalid credentials."}, status=status.HTTP_401_UNAUTHORIZED)
        return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)

    def get(self, request):
        serializer = self.serializer_class()
        return Response({'serializer': serializer.data})
    
    
    

class LogoutAPIView(APIView):
    def post(self, request):
        logout(request)
        return Response({'message': 'User logged out successfully'})
    
    

class HomePageView(APIView):
    def get(self, request):
        return Response({"message": "Welcome to the Home page."})

