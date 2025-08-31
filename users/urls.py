from django.urls import path

from users.views import UserListCreateAPIView, UserRetrieveUpdateDestroyAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name


urlpatterns = [
    path('', UserListCreateAPIView.as_view(), name='user_list'),
    path('<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user_detail'),
]
