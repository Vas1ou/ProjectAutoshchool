from django.shortcuts import render


def submit_documents(request):
    return render(request, 'submit_documents.html', context={})
