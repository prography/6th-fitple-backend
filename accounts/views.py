from rest_framework import status
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework_jwt.utils import jwt_decode_handler
from .serializers import UserCreateSerializer, UserLoginSerializer, ProfilePageSerializer
from .models import User, Profile


@api_view(['POST'])
@permission_classes([AllowAny])
def createUser(request):  # 회원가입 ?
    '''
    (req)
    email
    username
    password
    passwordCheck -- pass
    (res)
    message

    :param request:
    :return:
    '''
    if request.method == 'POST':
        # password_check = request.data.pop('passwordCheck')  #
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        # 앞 단에서 email 중복 체크하는데 여기도 있으면 좋은가 ? -- 물어보기
        # 비밀번호 1차 + 2차 같은지도 확인하기! -- 프론트에서도 할 수 있는 일인듯! 일단 코드만 작성해둘건데 구분 어떻게 하는지 물어보기!
        result_passwd_check = True  # serializer.validated_data['password'] == password_check  #
        if User.objects.filter(email=serializer.validated_data['email']).first() is None and result_passwd_check:  #
            serializer.save()  # 추가로 멤버 주입할 수 있었던듯
            # existing instance 제공하면 update 실행된다
            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response({"message": "duplicate email"}, status=status.HTTP_409_CONFLICT)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    '''
    (req)
    email
    password
    (res)
    success
    username
    token

    :param request:
    :return:
    '''
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        # query = User.objects.filter(email=serializer.validated_data['email']).first()
        query = User.objects.filter(email=serializer.validated_data['email']).values()[0]
        # print(query)
        # values()[0]

        username = query['username']
        # username = 'test'

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


class ProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    # profile -- read/update 가 달랐던가 ? 예를 들어, 이메일을 수정 안하려면 다르겠지 !
    serializer_class = ProfilePageSerializer

    # queryset 속성이 필요한가 ? list 도 아닌데 ?

    def retrieve(self, request, *args, **kwargs):
        '''
        (req)
        header - token
        (res)
        username
        livingArea
        phone
        email
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''

        # print('뷰 함수')
        user = request.user
        profile = Profile.objects.get(user=user)
        response = {
            'success': 'True',
            'username': user.username,
            'livingArea': profile.livingArea,
            'phone': profile.phone,
            'email': user.email
        }
        return Response(response, status=status.HTTP_200_OK)

    def update(self, request, *args, **kwargs):
        '''
        (req)
        username
        livingArea
        phone
        email
        (res)
        message : OK, Fail(409)
        :param request:
        :param args:
        :param kwargs:
        :return:
        '''
        # user = request.user  # User.objects.filter(email=request.data['email']).first()
        serializer = self.get_serializer(instance=request.user, data=request.data)
        # User 로 참조하기

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        serializer.save()  # User, Profile 변경

        # 잘 변경됐으면 return OK -- update OK 상태코드는 뭘까 ? 200 인듯
        return Response({"message": "ok."}, status=status.HTTP_200_OK) #
        # 아니면 return Fail
