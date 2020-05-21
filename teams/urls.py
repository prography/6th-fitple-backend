from django.urls import path, include
from rest_framework.routers import DefaultRouter
from teams import views


router = DefaultRouter()
router.register(r'', views.TeamViewSet)

urlpatterns = [
    path(r'', include(router.urls))
]