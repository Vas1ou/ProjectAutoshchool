from django.http import HttpResponse
from django.shortcuts import render
from django.contrib.auth.hashers import make_password

from .utils import is_valid_phone_number
from .models import StudentProfile, User


def registration(request):
    if request.method == 'POST':
        data = {
            'fist_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'password': request.POST.get('password'),
            'repeat_password': request.POST.get('repeat_password'),
            'ph_number': request.POST.get('ph_number'),
            'date_birth': request.POST.get('date_birth'),
        }
        print(data)
        # Проверка, что пароли одинаковые
        if data['password'] != data['repeat_password']:
            return render(request, 'registration.html', {'error_password': 'Пароли не совпадают'})
        # Проверка, что номер телефона валидный
        if not is_valid_phone_number(data['ph_number']):
            return render(request, 'registration.html',
                          {'error_password': 'Номер телефона введён неправильно'})
        # Проверка, что пользователь с таким номером телефона отсутствует
        if User.objects.filter(phone=data['ph_number']).exists():
            return render(request, 'registration.html',
                          {'error_password': 'Пользователь с таким номером телефона уже существует'})

        # Создание пользователя
        StudentProfile.objects.create(
            first_name=data['fist_name'],
            last_name=data['last_name'],
            phone=data['ph_number'],
            password=make_password(data['password']),
            is_active=False,# Хешируем пароль
            date_of_birth=data['date_birth']
        )

        return HttpResponse("СПАСИБО ВАШИ ДАННЫЕ УШЛИ НА СЕРВЕР")
    elif request.method == 'GET':
        return render(request, 'registration.html', {})
