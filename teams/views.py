from django.shortcuts import render
from rest_framework import viewsets
from rest_framework import status
from rest_framework import permissions
from rest_framework.response import Response
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

    def create(self, request, *args, **kwargs):
        try:
            serializer = self.get_serializer(data=request.data)
            serializer.is_valid(raise_exception=True)
            self.perform_create(serializer)
            headers = self.get_success_headers(serializer.data)
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except:
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

    def perform_create(self, serializer):
        serializer.save(author=self.request.user)


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
            return Response(serializer.data, status=status.HTTP_201_CREATED, headers=headers)
        except:
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)

    def perform_create(self, serializer):
        serializer.save(user=self.request.user)


class CommentOnlyViewSet(viewsets.ReadOnlyModelViewSet):
    queryset = Team.objects.all()
    serializer_class = TeamOnlyCommentSerializer
    permission_classes = [permissions.AllowAny]