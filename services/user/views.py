from rest_framework import status, generics
from .serializers import UserSerializer
from .models import User

from .components import get_user_by_id, get_all_users, create_user, update_user
from .components import *

from rest_framework.views import APIView
from rest_framework.response import Response

from rest_framework_simplejwt.tokens import RefreshToken
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.permissions import IsAuthenticated


class UserListView(generics.ListAPIView):

    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated]

    def get_queryset(self):
        return get_all_users()
    
class UserDetailView(generics.RetrieveAPIView):
    queryset = User.objects.all() 
    serializer_class = UserSerializer
    lookup_field = 'id'           # back here
    permission_classes=[IsAuthenticated]

class UserCreateView(generics.CreateAPIView):
    serializer_class = UserSerializer

    def perform_create(self, serializer):
        create_user(serializer.validated_data) 

class UserUpdateView(generics.UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated]

    def perform_update(self, serializer):
        update_user(serializer.validated_data) 

class UserDeleteView(generics.DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes=[IsAuthenticated]

class UserLoginView(APIView):
    def post(self, request):
        username = request.data.get('username')
        password = request.data.get('password')

        user = authenticate_user(username=username, password=password)
        if user:
            refresh = RefreshToken.for_user(user)
            access_token = str(refresh.access_token)

            return Response({
                'message': 'Login successful!',
                'access_token': access_token,
                'refresh_token': str(refresh)
            })   
        return Response({"error": "Invalid credentials!"}, status=status.HTTP_400_BAD_REQUEST)
