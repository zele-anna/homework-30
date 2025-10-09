from django.urls import reverse
from rest_framework import status
from rest_framework.test import APITestCase

from lms.models import Course, Lesson
from users.models import User


class CourseTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test1@example.com")
        self.course = Course.objects.create(title='Course 1', owner=self.user)
        self.lesson = Lesson.objects.create(title='Lesson 1', course=self.course, link='youtube.com/123',
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_course_create(self):
        '''Тестирование создания курса.'''
        data = {'title': 'Test course 1'}
        response = self.client.post('/lms/', data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Course.objects.all().count(), 2)

    def test_course_retrieve(self):
        '''Тестирование получения информации по курсу.'''
        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), self.course.title)
        self.assertEqual(data.get('lesson_count'), 1)
        self.assertEqual(data.get('lessons')[0].get('title'), self.lesson.title)
        self.assertEqual(data.get('subscription'), False)

    def test_course_update(self):
        '''Тестирование изменения курса.'''
        url = reverse('lms:course-detail', args=(self.course.pk,))
        data = {'title': 'Test course update'}
        response = self.client.patch(url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Course.objects.all().count(), 1)
        self.assertEqual(result.get('title'), 'Test course update')

    def test_course_delete(self):
        '''Тестирование удаления курса.'''
        url = reverse('lms:course-detail', args=(self.course.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Course.objects.all().count(), 0)

    def test_course_list(self):
        '''Тестирование вывода списка курсов.'''
        response = self.client.get('/lms/')
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results':
                [
                    {
                        'pk': self.course.pk,
                        'title': 'Course 1',
                        'preview': None,
                        'description': None,
                        'lesson_count': 1,
                        'lessons':
                            [
                                {
                                    'id': self.lesson.pk,
                                    'title': 'Lesson 1'
                                }
                            ],
                        'subscription': False,
                        'updated_at': None
                    }
                ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), result)


class LessonTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test1@example.com")
        self.course = Course.objects.create(title='Course 1', owner=self.user)
        self.lesson = Lesson.objects.create(title='Lesson 1', course=self.course, link='youtube.com/123',
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_lesson_create(self):
        '''Тестирование создания урока.'''
        url = reverse('lms:lesson_create')
        data = {'title': 'Test lesson 1', 'link': 'youtube.com/sdfksd1er'}
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(Lesson.objects.all().count(), 2)

    def test_lesson_retrieve(self):
        '''Тестирование получения информации по уроку.'''
        url = reverse('lms:lesson_detail', args=(self.lesson.pk,))
        response = self.client.get(url)
        data = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('title'), self.lesson.title)

    def test_lesson_update(self):
        '''Тестирование изменения урока.'''
        url = reverse('lms:lesson_update', args=(self.lesson.pk,))
        data = {'title': 'Test lesson update', 'link': 'youtube.com/23425'}
        response = self.client.patch(url, data=data)
        result = response.json()

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(Lesson.objects.all().count(), 1)
        self.assertEqual(result.get('title'), 'Test lesson update')

    def test_lesson_delete(self):
        '''Тестирование удаления урока.'''
        url = reverse('lms:lesson_delete', args=(self.lesson.pk,))
        response = self.client.delete(url)

        self.assertEqual(response.status_code, status.HTTP_204_NO_CONTENT)
        self.assertEqual(Lesson.objects.all().count(), 0)

    def test_lesson_list(self):
        '''Тестирование вывода списка уроков.'''
        url = reverse('lms:lesson_list')
        response = self.client.get(url)
        result = {
            'count': 1,
            'next': None,
            'previous': None,
            'results': [
                {
                    'id': self.lesson.pk,
                    'title': 'Lesson 1',
                    'preview': None,
                    'description': None,
                    'link': 'youtube.com/123',
                    'updated_at': None,
                    'course': self.course.pk,
                    'owner': self.user.pk
                }
            ]
        }

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json(), result)


class SubscriptionTestCase(APITestCase):

    def setUp(self):
        self.user = User.objects.create(email="test1@example.com")
        self.course = Course.objects.create(title='Course 1', owner=self.user)
        self.lesson = Lesson.objects.create(title='Lesson 1', course=self.course, link='youtube.com/123',
                                            owner=self.user)
        self.client.force_authenticate(user=self.user)

    def test_subscribe(self):
        '''Тестирование функционала подписки.'''
        url = reverse('lms:subscription')
        data = {'course': self.course.pk}
        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), 'подписка добавлена')

        response = self.client.post(url, data=data)

        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.json().get('message'), 'подписка удалена')
