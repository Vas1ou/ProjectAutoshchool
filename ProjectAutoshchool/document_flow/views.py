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


def accept_documents(request, document_id):
    document = DocumentsAdmission.objects.get(pk=document_id)
    if request.method == 'GET':
        return render(request, 'accept_documents.html', context={'document': document})
    else:
        # Переменная отвечает за документы (приняты или нет)
        action = request.POST.get('action')
        # Получаю студента
        student = document.user
        # Если документы не приняты
        if action == 'reject':
            # Если документы не приняты, необходимо удалить документы, а у студента отобразить то, что он не
            # подал документы
            student.submit_doc = False
            student.save()

            # Удаляем медиафайлы вручную
            if document.medical_certificate:
                document.medical_certificate.delete(save=False)
            if document.check_for_service:
                document.check_for_service.delete(save=False)
            # Удаляю, поданные студентом, документы
            document.delete()
        # Если документы приняты
        elif action == 'accept':
            # Принимаем студента на обучение
            student.accepted = True
            student.save()
            # Отмечаем, что документы приняты
            document.verified = True
            document.save()
        return redirect('viewing_documents')
