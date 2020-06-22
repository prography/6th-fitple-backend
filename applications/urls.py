from django.urls import path
from rest_framework.routers import DefaultRouter

from . import views

router = DefaultRouter()
router.register(r'', views.TeamApplicationViewSet)

urlpatterns = [
    # path('questions/', views.get_questions),
]
urlpatterns += router.urls
