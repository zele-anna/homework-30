from datetime import timedelta

from django.utils import timezone
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from rest_framework.views import APIView
from rest_framework.viewsets import ModelViewSet
from rest_framework.generics import CreateAPIView, RetrieveAPIView, ListAPIView, UpdateAPIView, DestroyAPIView, \
    get_object_or_404

from lms.models import Course, Lesson, Subscription
from lms.pagination import CustomPagination
from lms.serializers import CourseSerializer, LessonSerializer
from lms.tasks import send_update_notification
from users.permissions import IsModer, IsOwner


class CourseViewSet(ModelViewSet):
    queryset = Course.objects.all()
    serializer_class = CourseSerializer
    pagination_class = CustomPagination

    def get_permissions(self):
        if self.action in ['retrieve', 'update', 'partial_update']:
            self.permission_classes = [IsModer | IsOwner,]
        elif self.action == 'create':
            self.permission_classes = [~IsModer,]
        elif self.action == 'destroy':
            self.permission_classes = [~IsModer | IsOwner,]
        return [permission() for permission in self.permission_classes]

    def perform_create(self, serializer):
        course = serializer.save()
        course.owner = self.request.user
        course.save()

    def perform_update(self, serializer):
        course = serializer.save()
        last_update = course.updated_at
        current_update = timezone.now()
        four_hours_earlier = current_update - timedelta(hours=4)
        if not last_update or last_update <= four_hours_earlier:
            send_update_notification.delay(course.pk, course.title)

        course.updated_at = current_update
        course.save()

    def get_queryset(self):
        if IsModer().has_permission(self.request, self):
            return Course.objects.all()
        else:
            return Course.objects.filter(owner=self.request.user)


class LessonCreateAPIView(CreateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, ~IsModer,]

    def perform_create(self, serializer):
        lesson = serializer.save()
        lesson.owner = self.request.user
        lesson.save()


class LessonRetrieveAPIView(RetrieveAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner,]

    def get_queryset(self):
        if IsModer().has_permission(self.request, self):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonListAPIView(ListAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated]
    pagination_class = CustomPagination

    def get_queryset(self):
        if IsModer().has_permission(self.request, self):
            return Lesson.objects.all()
        else:
            return Lesson.objects.filter(owner=self.request.user)


class LessonUpdateAPIView(UpdateAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsModer | IsOwner,]

    def perform_update(self, serializer):
        lesson = serializer.save()
        course = lesson.course
        last_update = course.updated_at
        current_update = timezone.now()
        four_hours_earlier = current_update - timedelta(hours=4)
        if not last_update or last_update <= four_hours_earlier:
            send_update_notification.delay(course.pk, course.title)

        lesson.updated_at = current_update
        lesson.save()
        course.updated_at = current_update
        course.save()


class LessonDestroyAPIView(DestroyAPIView):
    queryset = Lesson.objects.all()
    serializer_class = LessonSerializer
    permission_classes = [IsAuthenticated, IsOwner,]


class SubscriptionAPIView(APIView):
    def post(self, *args, **kwargs):
        user = self.request.user
        course_id = self.request.data.get('course')
        course_item = get_object_or_404(Course, pk=course_id)
        subs_item = Subscription.objects.filter(user=user, course=course_item)

        # Если подписка у пользователя на этот курс есть - удаляем ее
        if subs_item.exists():
            subs_item.delete()
            message = 'подписка удалена'
        # Если подписки у пользователя на этот курс нет - создаем ее
        else:
            Subscription.objects.create(user=user, course=course_item)
            message = 'подписка добавлена'
        # Возвращаем ответ в API
        return Response({"message": message})
