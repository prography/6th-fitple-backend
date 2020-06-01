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
from applications.serializers import TeamApplicationSerializer




class TeamApplicationViewSet(viewsets.ModelViewSet):
    queryset = TeamApplication.objects.all()
    serializer_class = TeamApplicationSerializer
    permission_classes = [IsAuthenticated]


    # 승인/거절 api  # 팀 리더


