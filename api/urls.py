from django.urls import path
from .views import ListCreatePostView

urlpatterns = [
    path('posts/', ListCreatePostView.as_view())
]