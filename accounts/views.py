from rest_framework import status, permissions
from rest_framework.generics import RetrieveUpdateAPIView
from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes, action
from rest_framework.permissions import AllowAny, IsAuthenticated
from rest_framework.viewsets import GenericViewSet

from .serializers import UserCreateSerializer, UserLoginSerializer, ProfilePageSerializer
from .models import User, Profile
from teams.models import Team
from applications.models import TeamApplication
## 테스트
from .task import def_email, def_welcome_email

# 시간이 없어서 임시로 작업
from config.settings.production import MEDIA_URL


@api_view(['POST'])
@permission_classes([AllowAny])
def createUser(request):  # 회원가입 ?

    if request.method == 'POST':
        # password_check = request.data.pop('passwordCheck')  #
        serializer = UserCreateSerializer(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        # 앞 단에서 email 중복 체크하는데 여기도 있으면 좋은가 ? -- 물어보기
        # 비밀번호 1차 + 2차 같은지도 확인하기! -- 프론트에서도 할 수 있는 일인듯! 일단 코드만 작성해둘건데 구분 어떻게 하는지 물어보기!
        result_passwd_check = True  # serializer.validated_data['password'] == password_check  #
        if User.objects.filter(email=serializer.validated_data['email']).first() is None and result_passwd_check:  #
            user = serializer.save()  # 추가로 멤버 주입할 수 있었던듯
            # existing instance 제공하면 update 실행된다

            def_welcome_email.delay(user.email)  # 가입 인사 메일

            return Response({"message": "ok"}, status=status.HTTP_201_CREATED)
        return Response({"message": "duplicate email"}, status=status.HTTP_409_CONFLICT)


@api_view(['POST'])
@permission_classes([AllowAny])
def login(request):
    if request.method == 'POST':
        serializer = UserLoginSerializer(data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        if serializer.validated_data['email'] == "None":
            return Response({'message': 'fail'}, status=status.HTTP_200_OK)
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
            return Response({
                "message": "register",
                "email": email
            }, status=status.HTTP_200_OK)
        return Response({
            "message": "login",
            "email": email
        }, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([AllowAny])
def getProfile(request, pk, format=None):
    if request.method == "GET":
        profile = Profile.objects.filter(user=pk).values()[0]
        username = User.objects.filter(id=pk).values()[0]
        profile["email"] = username["email"]
        profile["username"] = username["username"]
        profile["image"] = MEDIA_URL + profile["image"]

        return Response(profile)


@api_view(['GET'])
@permission_classes([AllowAny])
def test(request):
    if request.method == "GET":
        print("test")
        def_email.delay()
        return Response({"test": "test"})


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def application(request):
    if request.method == "GET":
        user = request.user
        applications = TeamApplication.objects.filter(applicant=user).values()
        my_application_list = []

        for j in applications:
            team = Team.objects.get(id=j["team_id"])
            title = team.title
            description = team.description
            team_image = str(team.image)
            image = MEDIA_URL + team_image
            my_application_list.append({
                "id": j["id"],
                "team_id": j["team_id"],
                "title": title,
                "description": description,
                "image": image,
                "join_status": j["join_status"],
                "job": j["job"]
            })
        response = {
            'myApplication': my_application_list
        }
        return Response(response, status=status.HTTP_200_OK)


@api_view(['GET'])
@permission_classes([IsAuthenticated])
def myTeam(request):
    if request.method == "GET":
        user = request.user
        team = Team.objects.filter(author=user).values()
        if len(team) != 0:
            print(team[0])
        my_team_list = []

        for i in team:
            my_team_list.append({
                "team_id": i["id"],
                "title": i["title"],
                "description": i["description"],
                "created_at": i["created_at"],
                "image": MEDIA_URL + i["image"]
            })

        response = {
            'myTeam': my_team_list
        }
        return Response(response, status=status.HTTP_200_OK)


class ProfileView(RetrieveUpdateAPIView):
    permission_classes = [IsAuthenticated]
    # profile -- read/update 가 달랐던가 ? 예를 들어, 이메일을 수정 안하려면 다르겠지 !
    serializer_class = ProfilePageSerializer

    # queryset 속성이 필요한가 ? list 도 아닌데 ?

    def retrieve(self, request, *args, **kwargs):
        # print('뷰 함수')
        user = request.user
        profile = Profile.objects.get(user=user)

        response = {
            'success': 'True',
            'profile': {
                'username': user.username,
                'livingArea': profile.livingArea,
                'phone': profile.phone,
                'email': user.email,
                'introduce': profile.introduce,
                'image': profile.image.url,
                'email_subscribe': profile.email_subscribe
            }
        }
        return Response(response, status=status.HTTP_200_OK)

    ''' 프로필 update :: PUT http://127.0.0.1:8000/account/profile/{profile_pk}/ '''

    def update(self, request, *args, **kwargs):
        # user = request.user  # User.objects.filter(email=request.data['email']).first()
        serializer = self.get_serializer(instance=request.user, data=request.data)

        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

        serializer.save()  # User, Profile 변경

        # 잘 변경됐으면 return OK -- update OK 상태코드는 뭘까 ? 200 인듯
        return Response({"message": "ok."}, status=status.HTTP_200_OK)  #
        # 아니면 return Fail


# User + Profile : 합쳐 전달하는 get api 필요할까 ?

class EmailSubscriptionViewSet(GenericViewSet):
    # queryset = Team.objects.all()
    # serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticated]

    @action(methods=['get'], detail=False,
            url_path='subscribe', url_name='email-subscribe')  # IsTeamLeader
    def subscribe_to_email(self, request, *args, **kwargs):
        # request.user 를 통해 Profile 가져오기
        try:
            profile = Profile.objects.get(user=request.user)
        except:
            return Response({"message": "Not Found."}, status=status.HTTP_404_NOT_FOUND)

        # Profile 상태 변경하고 저장

        # 이미 구독중이라면
        if profile.email_subscribe:
            return Response({"message": "Already Subscribed."}, status=status.HTTP_400_BAD_REQUEST)

        profile.email_subscribe = True
        profile.save()

        return Response({"message": "ok."}, status=status.HTTP_200_OK)

    @action(methods=['get'], detail=False,
            url_path='unsubscribe', url_name='email-unsubscribe')  # IsTeamLeader
    def unsubscribe_to_email(self, request, *args, **kwargs):
        print('sisi')
        # request.user 를 통해 Profile 가져오기
        try:
            profile = Profile.objects.get(user=request.user)
        except:
            return Response({"message": "Not Found."}, status=status.HTTP_404_NOT_FOUND)

        # Profile 상태 변경하고 저장

        # 이미 구독취소중이라면
        if not profile.email_subscribe:
            return Response({"message": "Already Unsubscribing."}, status=status.HTTP_400_BAD_REQUEST)

        profile.email_subscribe = False
        profile.save()

        return Response({"message": "ok."}, status=status.HTTP_200_OK)
