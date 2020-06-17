from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

from applications.models import TeamApplication
from applications.permissions import IsTeamLeader, IsOwner
from applications.serializers import TeamApplicationSerializer
from .serializers import TeamSerializer, TeamListSerializer, CommentSerializer, TeamOnlyCommentSerializer
from .models import Team, Comment


# Create your views here.


class TeamViewSet(viewsets.ModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def get_serializer_class(self):
        if self.action == 'list':
            return TeamListSerializer
        return self.serializer_class

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)

    def create(self, request, *args, **kwargs):
        # debug ok
        try:

            serializer = self.get_serializer(data=request.data)

            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                "board": serializer.data,
                "author": serializer.data['author'],
                "application": False
            }, status=status.HTTP_201_CREATED, headers=headers)
        except:
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

    def retrieve(self, request, pk=None):
        applications = TeamApplication.objects.filter(team_id=pk).values("applicant__username")
        
        app_list = []
        for app in applications:
            app_list.append(app['applicant__username'])
        app_boolean = False

        if request.user.username in app_list:
            app_boolean = True

        #applicants_user = [apc.applicant for apc in applications]


        instance = self.get_object()
        serializer = self.get_serializer(instance)
        return Response({
            "board": serializer.data,
            "author": serializer.data['author'],
            "application": app_boolean,
        })


    # 일단 다 가져오고 각각 커스텀 할 부분 생각하기
    @action(methods=['post', 'get'], detail=True,
            url_path='applications', url_name='about_applications',
            permission_classes=[IsAuthenticated])
    def create_and_list_application(self, request, *args, **kwargs):  # 인증된 사용자
        if request.method == 'POST':
            '''
            header - token :: 지원자 정보
            url : POST  teams/{detail}/applications
            (req)
            # team : 어떻게 구분할 생각? -- 일단 team id
            applicant   job
            (res)
            # 신청자, 팀, ok :: {신청자 username} 가 {팀 title} 에 지원함.
            '''

            # 나는 해당 팀 신청 list 에서 email list 를 만들고 싶어 -- 사실 email 이 아니라 id 로 해도 마찬가지로 동작한다!
            # 그리고 동일한 팀에 직무 다르게 지원하는 것도 괜찮다면 로직 수정이 있어야 한다!
            applications = TeamApplication.objects.filter(team__id=kwargs['pk'])
            applicants_email = [apc.applicant.email for apc in applications]
            # print(applicants_email)
            if request.user.email in applicants_email:
                return Response({"message": "Duplicated applicant's email."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = TeamApplicationSerializer(data=request.data)
            # team 은 kwargs 에서 구분하고
            # 작성자는 request.user
            # 당장은 직무만 선택하는 로직 작성하자! -- 다른건 동작 확인하고 계획하자! -- 다른거래봤자 질문인데 3개만 제한해서 작성하기로 하자 -- 3개이하
            serializer.is_valid(raise_exception=True)
            team = Team.objects.get(pk=kwargs['pk'])
            # 신청한 직무에 대해 초과 인원 뺄 필요가 당장은 없겠다 -- 의식의흐름... 일단 다 신청받기
            serializer.save(team=team, applicant=request.user)

            response = {
                # "message": f"'{self.request.user.username}' applies to Team: '{team.title}'"
                "message": "ok"
            }
            headers = self.get_success_headers(serializer.data)
            return Response(response, status=status.HTTP_201_CREATED, headers=headers)

        elif request.method == 'GET':
            '''
            이 api 는 팀 리더가 마이페이지에서
            팀 리더가 생성한 Team list 를 먼저 보고
            하나를 선택해서 해당 팀 내의 신청 list 를 받는 api
            (req)
            url : GET  teams/{detail}/applications 라고 생각했는데
            동원오빠 url 에 맞춰서 작성하자
            
            근데 현재 작성한 api 는 쿼리 날리고 퍼미션을 검사하기 때문에
            퍼미션을 먼저 검사할 방법 생각해봐야한다! 일단은 동작하게 해놨지만...
            '''
            # IsTeamLeader : object level permission 잘 동작하는지 확인해보기 -- post랑 같이 개별 퍼미션 적용할 수 있을리가...
            # 또 직접 작성해서 확인해보기

            # get_queryset 커스텀 해야할까...
            # 해당 팀에 관련된 신청 정보만 전달 !
            # 지원자가 취소한 데이터는 보여주지 말것

            queryset = TeamApplication.objects.filter(  # 해당 팀의 신청 정보를 먼저 가져오고
                team__id=kwargs['pk']
            ).exclude(  # 지원자가 취소한 신청 정보 필터링하기
                join_status=TeamApplication.CANCELED
            )

            application = queryset.first()
            if application is None:  # -- 퍼미션 검사하면서 None 객체에 접근하는 참사를 막기 위해 ?
                return Response({"message": "No results."}, status=status.HTTP_200_OK)

            permission = IsTeamLeader().has_object_permission(self.request, self, application.team)
            if permission is False:
                # 팀 객체 퍼미션 확인하기 -- 팀 리더가 요청했을 때만 신청 list 반환하려고
                return Response({"message": "Request Permission Error."}, status=status.HTTP_403_FORBIDDEN)

            serializer = TeamApplicationSerializer(instance=queryset, many=True)
            team_serializer = TeamSerializer(instance=application.team)

            response = {
                'team': team_serializer.data['id'],
                'applications': serializer.data
            }
            return Response(response, status=status.HTTP_200_OK)

        return Response({"message": "method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)

    @action(methods=['get', 'put', 'delete'], detail=True, url_path='applications/(?P<application_id>\d+)',
            url_name='detail_applications', permission_classes=[IsOwner])
    def retrieve_update_cancel_application(self, request, *args, **kwargs):  # 인증된 사용자
        if request.method == 'GET':
            '''
            url : GET  teams/{detail:팀id}/applications/{detail:신청id}
            '''
            # update 위해 화면에 뿌려줄 기존 데이터

            # 해당 팀에 대해 작성한 내 기존 데이터 불러오기
            # 이게 되려면 create 할 때 중복이 없어야 한다!
            try:
                application = TeamApplication.objects.get(pk=kwargs['application_id'])
            except:
                return Response({"message": "Not Found."}, status=status.HTTP_404_NOT_FOUND)

            # 인증된 사용자라도 자기자신이 아닐 수 있다 -- permission 확인
            permission = IsOwner().has_object_permission(self.request, self, application)
            if application is not None and permission is False:
                return Response({"message": "Request Permission Error."}, status=status.HTTP_403_FORBIDDEN)
            # self.check_object_permissions(self.request, application)

            serializer = TeamApplicationSerializer(instance=application)
            return Response(serializer.data, status=status.HTTP_200_OK)

        elif request.method == 'PUT':
            '''
            url : PUT  teams/{detail}/applications/{detail}
            '''
            # 신청 정보 수정
            # 대기중 일 때만 가능해야겠지
            # 퍼미션 먼저 확인 -- 객체 찾고 가능

            # 객체 존재 확인
            try:
                application = TeamApplication.objects.get(pk=kwargs['application_id'])
            except:
                return Response({"message": "Not Found."}, status=status.HTTP_404_NOT_FOUND)

            # 퍼미션 확인
            permission = IsOwner().has_object_permission(self.request, self, application)
            if permission is False:
                return Response({"message": "Request Permission Error."}, status=status.HTTP_403_FORBIDDEN)
            # self.check_object_permissions(self.request, application)

            # 상태가 대기중일 때만 수정 가능
            if application.join_status != TeamApplication.WAITING:
                return Response({"message": "Bad Request."}, status=status.HTTP_400_BAD_REQUEST)

            serializer = TeamApplicationSerializer(instance=application, data=self.request.data)
            serializer.is_valid(raise_exception=True)
            serializer.save()  # update() 호출

            # 상세 반환 메시지 생각! ok
            return Response({"message": "ok"}, status=status.HTTP_200_OK)

        elif request.method == 'DELETE':
            '''
            url : DELETE  teams/{detail}/applications/{detail}
            '''
            try:
                application = TeamApplication.objects.get(pk=kwargs['application_id'])
            except:
                return Response({"message": "Not Found."}, status=status.HTTP_404_NOT_FOUND)

            # 퍼미션 확인
            permission = IsOwner().has_object_permission(self.request, self, application)
            if permission is False:
                return Response({"message": "Request Permission Error."}, status=status.HTTP_403_FORBIDDEN)
            # self.check_object_permissions(self.request, application)

            # 실제로 삭제하지말고 취소상태로 바꾸기
            application.join_status = TeamApplication.CANCELED
            application.save()

            return Response({"message": "ok"}, status=status.HTTP_200_OK)

        return Response({"message": "method not allowed."}, status=status.HTTP_405_METHOD_NOT_ALLOWED)


class CommentViewSet(viewsets.ModelViewSet):
    queryset = Comment.objects.all()
    serializer_class = CommentSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response({
                "team_id": serializer.data["team"],
                "message": "ok"
            }, status=status.HTTP_201_CREATED, headers=headers)
        except:
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamOnlyCommentSerializer
    permission_classes = [permissions.AllowAny]
