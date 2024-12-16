from django.contrib.auth import authenticate, logout, login
from django.contrib.auth.decorators import login_required
from django.http import HttpResponse
from django.shortcuts import render, redirect
from django.contrib.auth.hashers import make_password

from .utils import is_valid_phone_number
from .models import StudentProfile, User, StudentGroup


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
        return render(request, 'registration.html', {'title': 'Регистрация'})



def login_user(request):
    if request.method == 'GET':
        return render(request, 'login.html', {'title': 'Авторизация'})
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
            return render(request, 'login.html', {'error': error_message,
                                                                      'title': 'Авторизация'})


@login_required
def logout_user(request):
    logout(request)
    return redirect('general')


def add_group(request):
    context = {'title': 'Добавить группу'}
    if request.method == 'GET':
        return render(request, 'add_group.html', context=context)
    elif request.method == 'POST':
        name = request.POST.get('name')
        try:
            group_capacity = int(request.POST.get('group_capacity').strip())
        except Exception:
            context['error'] = 'Введите количество учащихся для данной группы'
            return render(request, 'add_group.html', context=context)
        if StudentGroup.objects.filter(name=name).exists():
            context['error'] = 'Группа с таким названием уже существует. '
            return render(request, 'add_group.html', context=context)
        StudentGroup.objects.create(name=name, group_capacity=group_capacity)

        return redirect('general')


def get_groups(request):
    groups = StudentGroup.objects.all()
    context = {'title': 'Просмотр всех групп', 'groups': groups}
    return render(request, 'get_groups.html', context=context)