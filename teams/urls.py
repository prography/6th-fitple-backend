from django.urls import path, include
from rest_framework.routers import DefaultRouter
from teams import views


router = DefaultRouter()
router.register(r'', views.TeamViewSet)
router.register(r'comments', views.CommentViewSet)

urlpatterns = [
    path(r'', include(router.urls))
]