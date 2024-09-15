from django.shortcuts import render, redirect
from .models import DocumentsAdmission


def submit_documents(request):
    if request.method == 'GET':
        return render(request, 'submit_documents.html', context={})

    elif request.method == 'POST':
        data = {
            'passport_series': request.POST.get('passport_series'),
            'issued_by': request.POST.get('issued_by'),
            'when_issued': request.POST.get('when_issued'),
            'medical_certificate': request.FILES.get('medical_certificate'),
            'check_for_service': request.FILES.get('check_for_service'),
            'user_id': request.user.id
        }
        print(data)
        DocumentsAdmission.objects.create(**data)
        return redirect('general')
