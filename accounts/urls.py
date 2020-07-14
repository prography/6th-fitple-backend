from django.urls import path
from rest_framework.routers import DefaultRouter

from accounts.views import EmailSubscriptionViewSet
from . import views

email_router = DefaultRouter()
email_router.register(r'profile/email', EmailSubscriptionViewSet, basename='email-subscribe-api')

urlpatterns = [
    path('user/create/', views.createUser),
    path('user/login/', views.login),
    path('user/check/', views.userCheck),
    path('user/profile/<int:pk>/', views.getProfile),
    path('profile/', views.ProfileView.as_view()),
    path('profile/application/', views.application),
    path('profile/team/', views.myTeam),
    # path('profile/email/', email_router.urls),
    path('test/', views.test)  # celery email test
]
urlpatterns += email_router.urls
