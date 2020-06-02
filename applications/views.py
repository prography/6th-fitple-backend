from django.shortcuts import render
from rest_framework.decorators import action
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response

# 뷰를 어떻게 작성할지는 url 설계 생각하면서도 바뀔 수 있구나

# 지원자가
# TeamApplication 생성 -- 신청 api
# 지원 수정 api -- 도 가능하게 !
# 지원 취소 api

# 팀 생성자가
# 지원자를 승인/거절 api
# approve refuse
from rest_framework import viewsets, status

from applications.models import TeamApplication
from applications.permissions import IsTeamLeader, IsApplicationTeamLeader
from applications.serializers import TeamApplicationSerializer


class TeamApplicationViewSet(viewsets.GenericViewSet):
    queryset = TeamApplication.objects.all()
    serializer_class = TeamApplicationSerializer
    permission_classes = [IsApplicationTeamLeader]

    # 승인/거절 api  # 팀 리더
    '''
    url : GET applications/{detail}/approve - refuse
    '''

    @action(methods=['get'], detail=True, url_path='approve',
            url_name='approve_application')
    def approve_application(self, request, *args, **kwargs):
        # pk 가 TeamApplication 거니까
        # 객체 가져와서 상태만 변경하면 되겠지 ?
        # try:
        application = self.get_object()  # not found ? -- TODO 에러잡기
        # print(application)
        # except:
        #     return Response({"message": "not found."}, status=status.HTTP_404_NOT_FOUND)
        # not found + permission 에러 한 번에 못잡는다

        if application.join_status == TeamApplication.WAITING:
            application.join_status = TeamApplication.APPROVED
            application.save()
            # print(application)
            # serializer = self.get_serializer(application)
            # print(serializer.data)
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        return Response({"message": "Application Status Error."}, status=status.HTTP_400_BAD_REQUEST)

    @action(methods=['get'], detail=True, url_path='refuse',
            url_name='refuse_application')
    def refuse_application(self, request, *args, **kwargs):
        application = self.get_object()

        if application.join_status == TeamApplication.WAITING:
            application.join_status = TeamApplication.REJECTED
            application.save()

            # serializer = self.get_serializer(application)
            # print(serializer.data)
            return Response({"message": "ok"}, status=status.HTTP_200_OK)
        return Response({"message": "Application Status Error."}, status=status.HTTP_400_BAD_REQUEST)
