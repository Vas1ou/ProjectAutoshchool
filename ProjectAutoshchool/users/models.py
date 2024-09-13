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

    def save(self, *args, **kwargs):
        super().save(*args, **kwargs)


class TeacherProfile(User):
    bio = models.TextField(blank=True, null=True)


class ManagerProfile(User):
    def save(self, *args, **kwargs):
        if not self.pk:  # При первом сохранении
            self.user_type = 'manager'
        super().save(*args, **kwargs)

    class Meta:
        verbose_name = 'Manager'
        verbose_name_plural = 'Managers'


class StudentProfile(User):
    address = models.TextField(blank=True, null=True)
    date_of_birth = models.DateField(blank=True, null=True)
    accepted = models.BooleanField(null=False, default=False)

    def save(self, *args, **kwargs):
        if not self.pk:  # При первом сохранении
            self.user_type = 'student'
        super().save(*args, **kwargs)
