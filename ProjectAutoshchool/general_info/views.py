from django.shortcuts import render


def general(request):
    context = {}
    return render(request, 'general.html', context=context)


def about_us(request):
    return render(request, 'about_us.html', context={})
