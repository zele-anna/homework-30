from django.urls import path

from users.views import UserListCreateAPIView, UserRetrieveUpdateDestroyAPIView, PaymentListAPIView
from users.apps import UsersConfig

app_name = UsersConfig.name


urlpatterns = [
    path('', UserListCreateAPIView.as_view(), name='user_list'),
    path('<int:pk>/', UserRetrieveUpdateDestroyAPIView.as_view(), name='user_detail'),
    path('payments/', PaymentListAPIView.as_view(), name='payments'),
]
