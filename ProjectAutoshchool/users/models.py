from django.db import models
from django.contrib.auth.models import AbstractUser


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('manager', 'Manager'),
    )
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES, verbose_name='Тип пользователя')
    phone = models.CharField(max_length=15, blank=True, verbose_name='Номер телефона')

    def __str__(self):
        return self.username


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='teacher_profile')
    bio = models.TextField(blank=True, null=True)

    def __str__(self):
        return f'{self.user.username} (Учитель)'


class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='manager_profile')

    def __str__(self):
        return f'{self.user.username} (Менеджер)'


class StudentGroup(models.Model):
    """
    Группа студентов
    """

    name = models.CharField(max_length=100, unique=True, verbose_name='Название группы')
    group_capacity = models.IntegerField(verbose_name='Вместимость группы')
    group_is_raining = models.BooleanField(verbose_name='Группа на обучении', default=False)
    admission_to_test = models.BooleanField(default=False, verbose_name='Группа допущена к тестам')
    admission_to_exam = models.BooleanField(default=False, verbose_name='Группа допущена к экзамену')

    def __str__(self):
        return f'Группа {self.name}'

    @property
    def possibility_of_filling(self):
        return self.group_capacity > self.students.count() and not self.group_is_raining


class StudentProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, related_name='student_profile')
    address = models.TextField(blank=True, null=True, verbose_name='Адрес')
    date_of_birth = models.DateField(blank=True, null=True, verbose_name='Дата рождения')
    accepted = models.BooleanField(default=False, verbose_name='Студент принят на обучение?')
    submit_doc = models.BooleanField(default=False, verbose_name='Подал ли студент документы?')
    group = models.ForeignKey(StudentGroup, on_delete=models.CASCADE, related_name='students', null=True)

    def __str__(self):
        return f'{self.user.username} (Студент)'
