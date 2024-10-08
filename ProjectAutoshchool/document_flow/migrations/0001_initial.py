# Generated by Django 5.0.7 on 2024-09-28 09:35

import django.db.models.deletion
from django.db import migrations, models


class Migration(migrations.Migration):

    initial = True

    dependencies = [
        ('users', '0001_initial'),
    ]

    operations = [
        migrations.CreateModel(
            name='DocumentsAdmission',
            fields=[
                ('id', models.BigAutoField(auto_created=True, primary_key=True, serialize=False, verbose_name='ID')),
                ('passport_series', models.CharField(max_length=100, verbose_name='Серия и номер паспорта')),
                ('issued_by', models.CharField(max_length=255, verbose_name='Кем выдан документ')),
                ('when_issued', models.DateField(verbose_name='Когда выдан')),
                ('medical_certificate', models.ImageField(upload_to='documents/medical_cerf/', verbose_name='Мед. справка')),
                ('check_for_service', models.ImageField(upload_to='documents/checks/', verbose_name='Чек об оплате')),
                ('verified', models.BooleanField(default=False, verbose_name='Документы приняты')),
                ('user', models.ForeignKey(null=True, on_delete=django.db.models.deletion.SET_NULL, to='users.studentprofile')),
            ],
        ),
    ]
