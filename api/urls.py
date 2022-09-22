from django.urls import path
from rest_framework_simplejwt.views import TokenObtainPairView, TokenRefreshView
from .views import UserRegisterView, CreatePostView, ListUpdateDestroyPostView, UserConfigView

urlpatterns = [
    path('token/', TokenObtainPairView.as_view()),
    path('token/refresh/', TokenRefreshView.as_view()),
    path('register/', UserRegisterView.as_view()),
    path('posts/', CreatePostView.as_view()),
    path('posts/<int:pk>/', ListUpdateDestroyPostView.as_view()),
    path('user/<int:pk>/', UserConfigView.as_view()),
]