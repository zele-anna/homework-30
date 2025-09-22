from datetime import timedelta
from typing import Any

from celery import shared_task
from django.core.mail import send_mail
from django.utils import timezone

from config.settings import EMAIL_HOST_USER
from lms.models import Subscription
from users.models import User


@shared_task
def send_update_notification(course_pk):
    '''Задача по отправке уведомления об обновлении материалов курса.'''
    subscriptions = Subscription.objects.filter(course=course_pk)
    email_list = []
    for subscription in subscriptions:
        email_list.append(subscription.user.email)

    if email_list:
        subject = 'Обновление курса!'
        message = f'Материалы курса, на который Вы подписаны, обновлены!'
        send_mail(subject, message, EMAIL_HOST_USER, email_list)

@shared_task
def block_user_without_login_one_month():
    '''Задача по блокировке пользователя, который не заходил на платформу более месяца.'''
    users = User.objects.filter(is_superuser=False, is_staff=False, is_active=True)
    today = timezone.now()
    one_month_earlier = today - timedelta(days=30)
    for user in users:
        last_login = user.last_login
        date_joined = user.date_joined

        if last_login and last_login < one_month_earlier:
            user.is_active = False
            user.save()
        elif date_joined < one_month_earlier:
            user.is_active = False
            user.save()
