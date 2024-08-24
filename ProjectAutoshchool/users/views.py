from django.http import HttpResponse
from django.shortcuts import render


def registration(request):
    if request.method == 'POST':
        data = {
            'login': request.POST.get('login'),
            'password': request.POST.get('password'),
            'repeat_password': request.POST.get('repeat_password'),
            'ph_number': request.POST.get('ph_number'),
            'date_birth': request.POST.get('date_birth'),
        }

        if data['password'] != data['repeat_password']:
            return render(request, 'registration.html', {'error_password': 'Пароли не совпадают'})


        return HttpResponse("СПАСИБО ВАШИ ДАННЫЕ УШЛИ НА СЕРВЕР")
    elif request.method == 'GET':
        print('ДАННЫЕ С СЕРВЕРА ОТПРАВИЛИСЬ')
        return render(request, 'registration.html', {})
