from django.shortcuts import render, redirect
from .models import DocumentsAdmission
from users.models import StudentGroup


def submit_documents(request):
    if request.method == 'GET':
        return render(request, 'submit_documents.html', context={'title': 'Подача документов'})

    elif request.method == 'POST':
        student = request.user.student_profile
        data = {
            'passport_series': request.POST.get('passport_series'),
            'issued_by': request.POST.get('issued_by'),
            'when_issued': request.POST.get('when_issued'),
            'medical_certificate': request.FILES.get('medical_certificate'),
            'check_for_service': request.FILES.get('check_for_service'),
            'user': student
        }
        student.submit_doc = True
        student.save()
        DocumentsAdmission.objects.create(**data)
        return redirect('general')


def viewing_documents(request):
    documents = DocumentsAdmission.objects.filter(verified=False)
    context = {
        'documents': documents,
        'title': 'Просмотр документов'
    }
    return render(request, 'viewing_documents.html', context=context)


def accept_documents(request, document_id):
    document = DocumentsAdmission.objects.get(pk=document_id)
    if request.method == 'GET':
        context = {
            'title': 'Принять документы',
            'document': document,
            'groups': [group for group in StudentGroup.objects.all() if group.possibility_of_filling]
        }
        return render(request, 'accept_documents.html', context=context)
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
            student.group_id = request.POST.get('student_group')
            student.save()
            # Отмечаем, что документы приняты
            document.verified = True
            document.save()
        return redirect('viewing_documents')
