from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view
from .serializers import UserCreateSerializer, UserLoginSerializer
from .models import User


@api_view(['POST'])
def createUser(request):
    if request.method == 'POST':
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return
        if User.objects.filter(email=serializer.validated_data['email']).first() is None:
            serializer.save()
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response({"message": "duplicate email"}, status=status.HTTP_409_CONFLICT)


@api_view(['POST'])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return
        #query = User.objects.filter(email=serializer.validated_data['email']).first()
        query = User.objects.filter(email=serializer.validated_data['email']).values()[0]
        #print(query)
        #values()[0]

        username = query['username']
        #username = 'test'

        response = {
            'success': 'True',
            'username': username,
            'token': serializer.data['token']
        }
        return Response(response, status=status.HTTP_200_OK)


@api_view(['POST'])
def userCheck(request):
    if request.method == 'POST':
        email = request.data['email']

        if User.objects.filter(email=email).first() is None:
            return Response({"message": "register"}, status=status.HTTP_200_OK)
        return Response({"message": "login"}, status=status.HTTP_200_OK)