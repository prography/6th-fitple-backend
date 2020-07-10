# from django.shortcuts import render
# from rest_framework import viewsets
# from rest_framework.permissions import AllowAny
# from .serializers import FeedbackSerializers
# from .models import Feedback
# from rest_framework.decorators import permission_classes
#
# # Create your views here.
#
#
# class FeedbackViewset(viewsets.ModelViewSet):
#     queryset = Feedback.objects.all()
#     serializer_class = FeedbackSerializers
#     permissions_classes = [AllowAny]

from rest_framework.response import Response
from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import AllowAny
from .serializers import FeedbackSerializers
from .models import Feedback
from rest_framework import status


@api_view(['POST'])
@permission_classes([AllowAny])
def createFeedback(request):
    if request.method == 'POST':
        print(request.data)
        serializer = FeedbackSerializers(data=request.data)
        if not serializer.is_valid(raise_exception=True):
            return Response({"message": "Request Body Error."}, status=status.HTTP_409_CONFLICT)
        serializer.save()
        return Response({"message": "ok"}, status=status.HTTP_201_CREATED)