from rest_framework import status
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from rest_framework_jwt.utils import jwt_decode_handler
from .serializers import UserCreateSerializer, UserLoginSerializer
from .models import User


@api_view(['POST'])
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
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
@permission_classes([AllowAny])
def userCheck(request):
    if request.method == 'POST':
        email = request.data['email']

        if User.objects.filter(email=email).first() is None:
            return Response({"message": "register"}, status=status.HTTP_200_OK)
        return Response({"message": "login"}, status=status.HTTP_200_OK)


## permission 및 jwt 테스트
@api_view(['GET'])
def permissionTest(request):
    if request.method == 'GET':
        print(request.headers['Authorization'])
        authorization = request.headers['Authorization']
        authorization = authorization.replace("Bearer ", "")
        decoded_payload = jwt_decode_handler(authorization)

        return Response(decoded_payload)


