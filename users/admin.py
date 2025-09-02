from django.contrib import admin

from users.models import User, Payment

@admin.register(User)
class UserAdmin(admin.ModelAdmin):
    list_display = ("id", "email")


@admin.register(Payment)
class PaymentAdmin(admin.ModelAdmin):
    list_display = ('user', 'date', 'course', 'lesson', 'amount', 'payment_method')
