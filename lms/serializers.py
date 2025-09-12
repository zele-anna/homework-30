from rest_framework import serializers

from lms.models import Course, Lesson
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

    def get_lesson_count(self, course):
        return course.lesson_set.count()

    class Meta:
        model = Course
        fields = ['pk', 'title', 'preview', 'description', 'lesson_count', 'lessons']
