from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password

from .utils import is_valid_phone_number
from .models import StudentProfile, User


def registration(request):
    if request.method == 'POST':
        data = {
            'username': request.POST.get('login'),
            'first_name': request.POST.get('first_name'),
            'last_name': request.POST.get('last_name'),
            'password': request.POST.get('password'),
            'repeat_password': request.POST.get('repeat_password'),
            'phone': request.POST.get('ph_number'),
            'date_of_birth': request.POST.get('date_birth'),
        }

        # Проверка, что пароли одинаковые
        if data['password'] != data['repeat_password']:
            return render(request, 'registration.html', {'error': 'Пароли не совпадают'})
        # Проверка, что номер телефона валидный
        if not is_valid_phone_number(data['phone']):
            return render(request, 'registration.html',
                          {'error': 'Номер телефона введён неправильно'})
        # Проверка, что пользователь с таким номером телефона отсутствует
        if User.objects.filter(phone=data['phone']).exists():
            return render(request, 'registration.html',
                          {'error': 'Пользователь с таким номером телефона уже существует'})

        # Создание пользователя
        user = User.objects.create(
            username=data['username'],
            first_name=data['first_name'],
            last_name=data['last_name'],
            phone=data['phone'],
            password=make_password(data['password']),  # Хешируем пароль
            user_type='student'  # Устанавливаем тип пользователя
        )
        # Создание профиля студента
        StudentProfile.objects.create(
            user=user,  # Связываем профиль с пользователем
            date_of_birth=data['date_of_birth'],  # Дата рождения
            submit_doc=True,
        )
        return redirect('login_user')
    elif request.method == 'GET':
        return render(request, 'registration.html', {})



def login_user(request):
    if request.method == 'GET':
        return render(request, 'login.html', {})
    elif request.method == 'POST':
        username = request.POST.get('login')
        password = request.POST.get('password')

        # Аутентификация пользователя
        user = authenticate(username=username, password=password)

        if user is not None:
            # Вход пользователя
            login(request, user)
            return redirect('general')
        else:
            # Ошибка аутентификации
            error_message = "Неверный логин пользователя или пароль."
            return render(request, 'login.html', {'error': error_message})


@login_required
def logout_user(request):
    logout(request)
    return redirect('general')