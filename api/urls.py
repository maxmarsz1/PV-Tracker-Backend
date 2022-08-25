from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegisterView, ListCreatePostView, UpdateDestroyPostView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('register/', UserRegisterView.as_view()),
    path('posts/', ListCreatePostView.as_view()),
    path('posts/<int:pk>/', UpdateDestroyPostView.as_view()),
]