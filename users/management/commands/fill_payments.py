from django.core.management.base import BaseCommand

from lms.models import Course, Lesson
from users.models import Payment, User


class Command(BaseCommand):
    def handle(self, *args, **options):
        user = User.objects.create(email='2@mail.ru')
        course = Course.objects.create(title='Курс 3')
        lesson = Lesson.objects.create(title='Урок 15')

        data = [
            {
                'user': user,
                'date': '2025-08-27',
                'course': None,
                'lesson': None,
                'amount': 25000,
                'payment_method': 'наличные'
            },
            {
                'user': user,
                'date': '2025-08-29',
                'course': course,
                'lesson': None,
                'amount': 10000.99,
                'payment_method': 'перевод на счет'
            },
            {
                'user': user,
                'date': '2025-08-30',
                'course': None,
                'lesson': lesson,
                'amount': 2000.5,
                'payment_method': 'перевод на счет'
            },
        ]

        for payment in data:
            Payment.objects.create(**payment)
