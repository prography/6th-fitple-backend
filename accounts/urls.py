from django.urls import path
from . import views

urlpatterns = [
    path('user/create/', views.createUser),
    path('user/login/', views.login),
    path('user/check/', views.userCheck),
    path('user/profile/<int:pk>/', views.getProfile),
    path('profile/', views.ProfileView.as_view()),
    path('profile/application/', views.application),
    path('test/', views.test) # celery email test
]
