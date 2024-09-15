from django.db import models
from users.models import StudentProfile


class DocumentsAdmission(models.Model):
    passport_series = models.CharField(max_length=100, verbose_name='Серия и номер паспорта')
    issued_by = models.CharField(max_length=255, verbose_name='Кем выдан документ')
    when_issued = models.DateField(verbose_name='Когда выдан')
    medical_certificate = models.ImageField(upload_to='documents/medical_cerf/', verbose_name='Мед. справка')
    check_for_service = models.ImageField(upload_to='documents/checks/', verbose_name='Чек об оплате')
    user = models.ForeignKey(StudentProfile, on_delete=models.SET_NULL, null=True)
    verified = models.BooleanField(default=False)