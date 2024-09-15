from django.contrib import admin

from django.contrib import admin
from .models import User, ManagerProfile


class ManagerProfileAdmin(admin.ModelAdmin):
    list_display = ('username', 'first_name', 'last_name', 'phone', 'user_type')
    search_fields = ('username', 'first_name', 'last_name')

    # Исключаем поле user_type из формы
    exclude = ('user_type', 'groups', 'user_permissions', 'is_staff', 'is_superuser', 'last_login', 'date_joined')


# Регистрируем ManagerProfile в админке
admin.site.register(ManagerProfile, ManagerProfileAdmin)
