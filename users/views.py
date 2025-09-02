from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListCreateAPIView, RetrieveUpdateDestroyAPIView, ListAPIView

from users.models import User, Payment
from users.serializers import UserSerializer, PaymentSerializer


class UserListCreateAPIView(ListCreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserRetrieveUpdateDestroyAPIView(RetrieveUpdateDestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method',]
    ordering_fields = ['date',]
