from django.shortcuts import render, redirect
from .models import DocumentsAdmission
from users.models import StudentProfile


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
        student = StudentProfile.objects.get(user_id=data['user_id'])
        student.submit_doc = True
        student.save()
        data['user_id'] = student.pk
        DocumentsAdmission.objects.create(**data)
        return redirect('general')


def viewing_documents(request):
    documents = DocumentsAdmission.objects.filter(verified=False)
    return render(request, 'viewing_documents.html', context={'documents': documents})

def accept_documents(request, stud_id):
    return render(request, 'accept_documents.html', context={'stud_id': stud_id})
