from django.urls import path
from .views import ListCreatePostView, UpdateDestroyPostView

urlpatterns = [
    path('posts/', ListCreatePostView.as_view()),
    path('posts/<int:pk>/', UpdateDestroyPostView.as_view()),
]