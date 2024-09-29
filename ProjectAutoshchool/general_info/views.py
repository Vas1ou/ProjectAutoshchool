from django.shortcuts import render


def general(request):
    return render(request, 'general.html', context={})


def about_us(request):
    return render(request, 'about_us.html', context={})
