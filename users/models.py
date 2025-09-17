from django.contrib.auth.models import AbstractUser
from django.db import models

# from lms.models import Lesson, Course


class User(AbstractUser):
    username = None

    email = models.EmailField(unique=True, verbose_name='Почта')

    phone = models.CharField(max_length=20, blank=True, null=True, verbose_name='Телефон')
    city = models.CharField(max_length=100, blank=True, null=True, verbose_name='Город')
    avatar = models.ImageField(upload_to='users/avatars/', blank=True, null=True, verbose_name='Аватар')

    USERNAME_FIELD = 'email'
    REQUIRED_FIELDS = []

    class Meta:
        verbose_name = 'Пользователь'
        verbose_name_plural = 'Пользователи'

    def __str__(self):
        return self.email


class Payment(models.Model):
    from lms.models import Lesson, Course

    PAYMENT_METHOD_CHOICES = [
        ('наличные', 'наличные'),
        ('перевод на счет', 'перевод на счет'),
    ]

    user = models.ForeignKey(User, on_delete=models.CASCADE, blank=True, null=True, verbose_name='Пользователь')
    date = models.DateTimeField(blank=True, null=True, verbose_name='Дата и время платежа')
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Оплаченный курс')
    lesson = models.ForeignKey(Lesson, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Оплаченный урок')
    amount = models.PositiveIntegerField(blank=True, null=True, verbose_name='Сумма оплаты')
    payment_method = models.CharField(max_length=20, choices=PAYMENT_METHOD_CHOICES, verbose_name='Способ оплаты')
    session_id = models.CharField(max_length=255, blank=True, null=True, verbose_name='ID сессии')
    link = models.URLField(max_length=500, blank=True, null=True, verbose_name='Ссылка на оплату')

    class Meta:
        verbose_name = 'Оплата'
        verbose_name_plural = 'Оплаты'

    def __str__(self):
        return f'{self.date} {self.amount}'
