from django.db import models

from users.models import User


class Course(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название курса')
    preview = models.ImageField(upload_to='lms/courses/previews/', verbose_name='Превью', blank=True, null=True)
    description = models.TextField(verbose_name='Описание курса', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', blank=True, null=True)

    class Meta:
        verbose_name = 'Курс'
        verbose_name_plural = 'Курсы'

    def __str__(self):
        return self.title


class Lesson(models.Model):
    title = models.CharField(max_length=150, verbose_name='Название урока')
    preview = models.ImageField(upload_to='lms/lessons/previews/', verbose_name='Превью', blank=True, null=True)
    description = models.TextField(verbose_name='Описание урока', blank=True, null=True)
    link = models.CharField(max_length=255, verbose_name='Ссылка на видео', blank=True, null=True)
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, verbose_name='Курс', blank=True, null=True)
    owner = models.ForeignKey(User, on_delete=models.SET_NULL, verbose_name='Владелец', blank=True, null=True)

    class Meta:
        verbose_name = 'Урок'
        verbose_name_plural = 'Уроки'

    def __str__(self):
        return self.title


class Subscription(models.Model):
    course = models.ForeignKey(Course, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Курс')
    user = models.ForeignKey(User, on_delete=models.SET_NULL, blank=True, null=True, verbose_name='Пользователь')

    class Meta:
        verbose_name = 'Подписка'
        verbose_name_plural = 'Подписки'

    def __str__(self):
        return self.course.title
