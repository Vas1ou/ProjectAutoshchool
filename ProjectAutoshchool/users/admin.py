from django.contrib import admin
from django import forms
from .models import User, TeacherProfile, ManagerProfile, StudentProfile


# Форма для ограничения выбора типа пользователя
class UserForm(forms.ModelForm):
    class Meta:
        model = User
        fields = ['username', 'first_name', 'last_name', 'user_type', 'phone']

    def __init__(self, *args, **kwargs):
        super(UserForm, self).__init__(*args, **kwargs)
        # Ограничение выбора на только учителя и менеджера
        self.fields['user_type'].choices = [
            ('teacher', 'Teacher'),
            ('manager', 'Manager'),
        ]


# Инлайн для профиля учителя
class TeacherProfileInline(admin.StackedInline):
    model = TeacherProfile
    can_delete = False
    extra = 0


# Инлайн для профиля менеджера
class ManagerProfileInline(admin.StackedInline):
    model = ManagerProfile
    can_delete = False
    extra = 0


# Админка для модели пользователя
class UserAdmin(admin.ModelAdmin):
    form = UserForm
    list_display = ['username', 'first_name', 'last_name', 'user_type', 'phone']
    search_fields = ['username', 'first_name', 'last_name']

    # В зависимости от типа пользователя добавляем соответствующий инлайн
    def get_inlines(self, request, obj):
        if obj is not None:  # Только при редактировании
            if obj.user_type == 'teacher':
                return [TeacherProfileInline]
            elif obj.user_type == 'manager':
                return [ManagerProfileInline]
        return []

    def get_queryset(self, request):
        # Фильтрация: не показываем студентов при создании пользователя
        qs = super().get_queryset(request)
        return qs.exclude(user_type='student')

    # Переопределение метода сохранения
    def save_model(self, request, obj, form, change):
        super().save_model(request, obj, form, change)

        # Создаем профиль учителя или менеджера, если его нет
        if obj.user_type == 'teacher' and not hasattr(obj, 'teacher_profile'):
            TeacherProfile.objects.create(user=obj)
        elif obj.user_type == 'manager' and not hasattr(obj, 'manager_profile'):
            ManagerProfile.objects.create(user=obj)


# Админка для профиля студента
class StudentProfileAdmin(admin.ModelAdmin):
    list_display = ['user', 'address', 'date_of_birth', 'accepted', 'submit_doc']
    search_fields = ['user__username', 'user__first_name', 'user__last_name']

    # Отключаем возможность добавления и удаления студентов
    def has_add_permission(self, request):
        return False

    def has_delete_permission(self, request, obj=None):
        return False


# Регистрируем все модели в админке
admin.site.register(User, UserAdmin)
admin.site.register(TeacherProfile)
admin.site.register(ManagerProfile)
admin.site.register(StudentProfile, StudentProfileAdmin)
