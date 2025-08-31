from rest_framework import serializers

from lms.models import Course, Lesson


class LessonSerializer(serializers.ModelSerializer):

    class Meta:
        model = Lesson
        fields = '__all__'


class CourseSerializer(serializers.ModelSerializer):
    lesson_count = serializers.SerializerMethodField()
    lessons = serializers.SerializerMethodField()
    # lesson = LessonSerializer()

    def get_lessons(self, course):
        return [lesson.title for lesson in Lesson.objects.filter(course=course)]


    class Meta:
        model = Course
        fields = ['pk', 'title', 'preview', 'description', 'lesson_count', 'lessons']

    def get_lesson_count(self, course):
        return course.lesson_set.count()
