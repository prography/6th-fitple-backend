from django.urls import path, include
from rest_framework.routers import DefaultRouter
from teams import views


router = DefaultRouter()
router.register(r'board', views.TeamViewSet)
router.register(r'comments', views.CommentViewSet)
router.register(r'comment', views.CommentOnlyViewSet)

urlpatterns = [
    path('', include(router.urls))
]
