from rest_framework import serializers

from lms.models import Course, Lesson, Subscription
from lms.validators import LinkValidator


class LessonSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = '__all__'
        validators = [LinkValidator(field='link')]


class LessonShortSerializer(serializers.ModelSerializer):
    class Meta:
        model = Lesson
        fields = ['id', 'title']


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = LessonShortSerializer(source='lesson_set', many=True, read_only=True)
    subscription = serializers.SerializerMethodField()

    def get_lesson_count(self, course):
        return course.lesson_set.count()

    def get_subscription(self, course):
        user = self.context['request'].user
        return Subscription.objects.filter(user=user, course=course).exists()

    class Meta:
        model = Course
        fields = ['pk', 'title', 'preview', 'description', 'lesson_count', 'lessons', 'subscription', 'updated_at']
