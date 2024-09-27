from django.contrib.auth.admin import UserAdmin as BaseUserAdmin
from django.contrib import admin
from .models import User, TeacherProfile, ManagerProfile, StudentProfile


class UserAdmin(BaseUserAdmin):
    list_display = ('username', 'email', 'first_name', 'last_name', 'user_type', 'is_staff', 'is_active')
    list_filter = ('user_type', 'is_staff', 'is_active')

    fieldsets = (
        (None, {'fields': ('username', 'password')}),
        ('Personal info', {'fields': ('first_name', 'last_name', 'email', 'phone')}),
        ('Permissions', {'fields': ('is_active', 'is_staff', 'is_superuser')}),
        ('Role', {'fields': ('user_type',)}),
    )

    add_fieldsets = (
        (None, {
            'classes': ('wide',),
            'fields': (
            'username', 'password1', 'password2', 'email', 'first_name', 'last_name', 'phone', 'user_type', 'is_staff',
            'is_active')}
         ),
    )

    def formfield_for_dbfield(self, db_field, request, **kwargs):
        if db_field.name == 'user_type':
            kwargs['choices'] = [choice for choice in db_field.choices if choice[0] != 'student']
        return super().formfield_for_dbfield(db_field, request, **kwargs)


# Базовый класс админки для профилей
class BaseProfileAdmin(admin.ModelAdmin):
    # Настройка отображаемых полей для чтения
    readonly_fields = ('username', 'first_name', 'last_name', 'email', 'phone')

    # Поля из связанных моделей User
    def username(self, obj):
        return obj.user.username

    def first_name(self, obj):
        return obj.user.first_name

    def last_name(self, obj):
        return obj.user.last_name

    def email(self, obj):
        return obj.user.email

    def phone(self, obj):
        return obj.user.phone

    username.short_description = 'Имя пользователя'
    first_name.short_description = 'Имя'
    last_name.short_description = 'Фамилия'
    email.short_description = 'Email'
    phone.short_description = 'Номер телефона'

    # Отображение всех полей User в админке
    def get_readonly_fields(self, request, obj=None):
        # Добавляем все поля пользователя к `readonly_fields`
        user_fields = ('username', 'first_name', 'last_name', 'email', 'phone')
        return self.readonly_fields + user_fields

    # Настройка fieldsets для админки
    def get_fieldsets(self, request, obj=None):
        # Настраиваем группы полей для отображения
        fieldsets = (
            ('Пользовательская информация', {'fields': ('username', 'first_name', 'last_name', 'email', 'phone')}),
        )
        if hasattr(self, 'profile_fieldsets'):
            fieldsets += self.profile_fieldsets
        return fieldsets


# Админка для TeacherProfile
class TeacherProfileAdmin(BaseProfileAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone', 'bio')

    # Определяем специфичные для TeacherProfile поля
    profile_fieldsets = (
        ('Профиль учителя', {'fields': ('bio',)}),
    )


# Админка для ManagerProfile
class ManagerProfileAdmin(BaseProfileAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone')


# Админка для StudentProfile
class StudentProfileAdmin(BaseProfileAdmin):
    list_display = ('user', 'first_name', 'last_name', 'phone', 'address', 'date_of_birth', 'accepted', 'submit_doc')

    # Определяем специфичные для StudentProfile поля
    profile_fieldsets = (
        ('Профиль студента', {'fields': ('address', 'date_of_birth', 'accepted', 'submit_doc')}),
    )

    # Отключаем возможность добавления, изменения и удаления студентов в админке
    def has_add_permission(self, request):
        return False

    def has_change_permission(self, request, obj=None):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# Регистрация моделей в админке
admin.site.register(User, admin.ModelAdmin)  # Если у тебя есть кастомная UserAdmin, используй её
admin.site.register(TeacherProfile, TeacherProfileAdmin)
admin.site.register(ManagerProfile, ManagerProfileAdmin)
admin.site.register(StudentProfile, StudentProfileAdmin)
