from django_filters.rest_framework import DjangoFilterBackend
from rest_framework import filters
from rest_framework.generics import ListAPIView, CreateAPIView, RetrieveAPIView, UpdateAPIView, DestroyAPIView
from rest_framework.permissions import AllowAny, IsAuthenticated

from users.models import User, Payment
from users.permissions import IsMyProfile
from users.serializers import UserSerializer, PaymentSerializer, UserReadSerializer
from users.services import create_stripe_product_and_price, create_stripe_session


class UserListAPIView(ListAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer


class UserCreateAPIView(CreateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [AllowAny]

    def perform_create(self, serializer):
        user = serializer.save()
        user.is_active = True
        user.set_password(self.request.data.get('password'))
        user.save()


class UserRetrieveAPIView(RetrieveAPIView):
    queryset = User.objects.all()
    serializer_class = UserReadSerializer
    permission_classes = [IsAuthenticated, IsMyProfile]


class UserUpdateAPIView(UpdateAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsMyProfile]


class UserDestroyAPIView(DestroyAPIView):
    queryset = User.objects.all()
    serializer_class = UserSerializer
    permission_classes = [IsAuthenticated, IsMyProfile]


class PaymentListAPIView(ListAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    filter_backends = [DjangoFilterBackend, filters.OrderingFilter]
    filterset_fields = ['course', 'lesson', 'payment_method',]
    ordering_fields = ['date',]
    permission_classes = [IsAuthenticated]



class PaymentCreateAPIView(CreateAPIView):
    queryset = Payment.objects.all()
    serializer_class = PaymentSerializer
    permission_classes = [IsAuthenticated]

    def perform_create(self, serializer):
        payment = serializer.save(user=self.request.user)
        payment_method = payment.payment_method
        course = payment.course
        lesson = payment.lesson
        amount = payment.amount
        price = dict()

        if payment_method == 'наличные':
            payment.save()
        else:
            if course and amount:
                price = create_stripe_product_and_price(course, amount)
            elif lesson and amount:
                price = create_stripe_product_and_price(lesson, amount)
            else:
                print('введены не все значения')

            session_id, session_url = create_stripe_session(price)
            payment.session_id = session_id
            payment.link = session_url
            payment.save()
