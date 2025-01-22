from django.http import JsonResponse
from rest_framework import status, generics
from .serializers import UserSerializer
# from .models import User
from .serializers import UserSerializer
from .models import User

from .components import get_user_by_id, get_all_users, create_user, update_user
from .components import *

from rest_framework.views import APIView
from rest_framework.response import Response
from django.contrib.auth import authenticate


class UserListView(generics.ListAPIView):
    serializer_class = UserSerializer

    def get_queryset(self):
        return get_all_users()
    
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all() 
    serializer_class = UserSerializer
    lookup_field = 'user_id'  # Optional if you want custom lookup field

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        create_user(serializer.validated_data) 

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

    def perform_update(self, serializer):
        update_user(serializer.validated_data) 

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate(username=username, password=password)
        if user:
            return Response({"message": "Login successful!"})
        return Response({"error": "Invalid credentials!"}, status=status.HTTP_400_BAD_REQUEST)
