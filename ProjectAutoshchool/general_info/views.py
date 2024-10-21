from django.shortcuts import render


def general(request):
    return render(request, 'general.html', context={'title': 'Главная страница'})


def about_us(request):
    return render(request, 'about_us.html', context={'title': 'О нас'})
