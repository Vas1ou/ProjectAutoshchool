# Generated by Django 5.0.7 on 2024-09-15 10:05

from django.db import migrations, models


class Migration(migrations.Migration):

    dependencies = [
        ('users', '0002_alter_managerprofile_options'),
    ]

    operations = [
        migrations.AddField(
            model_name='studentprofile',
            name='submit_doc',
            field=models.BooleanField(default=False, verbose_name='Подал ли студент документы?'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='accepted',
            field=models.BooleanField(default=False, verbose_name='Студент принят на обучение?'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='address',
            field=models.TextField(blank=True, null=True, verbose_name='Адрес'),
        ),
        migrations.AlterField(
            model_name='studentprofile',
            name='date_of_birth',
            field=models.DateField(blank=True, null=True, verbose_name='Дата рождения'),
        ),
        migrations.AlterField(
            model_name='user',
            name='first_name',
            field=models.CharField(blank=True, db_index=True, max_length=50, verbose_name='Имя'),
        ),
        migrations.AlterField(
            model_name='user',
            name='last_name',
            field=models.CharField(blank=True, db_index=True, max_length=50, verbose_name='Фамилия'),
        ),
        migrations.AlterField(
            model_name='user',
            name='phone',
            field=models.CharField(blank=True, max_length=15, verbose_name='Номер телефона'),
        ),
        migrations.AlterField(
            model_name='user',
            name='user_type',
            field=models.CharField(choices=[('student', 'Student'), ('teacher', 'Teacher'), ('manager', 'Manager')], max_length=10, verbose_name='Тип пользователя'),
        ),
    ]
