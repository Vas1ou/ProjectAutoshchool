from django.db import models
from django.contrib.auth.models import AbstractUser, Group, Permission


class User(AbstractUser):
    USER_TYPE_CHOICES = (
        ('student', 'Student'),
        ('teacher', 'Teacher'),
        ('manager', 'Manager'),
    )
    first_name = models.CharField(max_length=50, blank=True, db_index=True)
    last_name = models.CharField(max_length=50, blank=True, db_index=True)
    user_type = models.CharField(max_length=10, choices=USER_TYPE_CHOICES)
    phone = models.CharField(max_length=15, blank=True)

    # Указываем уникальные related_name для устранения конфликта
    groups = models.ManyToManyField(Group, related_name='custom_user_set')
    user_permissions = models.ManyToManyField(Permission, related_name='custom_user_permissions_set')


class TeacherProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'teacher'}, related_name='teacher_profile')
    bio = models.TextField(blank=True, null=True)


class ManagerProfile(models.Model):
    user = models.OneToOneField(User, on_delete=models.CASCADE, limit_choices_to={'user_type': 'manager'}, related_name='manager_profile')
    address = models.TextField(blank=True, null=True)


class StudentProfile(User):
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    accepted = models.BooleanField(null=False, default=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # При первом сохранении
            self.user_type = 'student'
        super().save(*args, **kwargs)
