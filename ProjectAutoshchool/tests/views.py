from django.shortcuts import render
from .models import Question


# количество вариантов ответов
NUMBER_OF_RESPONSES = 4


def add_question(request):
    if request.method == 'GET':
        context = {
            'title': 'Создать вопрос',
            'number_of_responses': range(1, NUMBER_OF_RESPONSES + 1)
        }
    elif request.method == 'POST':
        question_data = {
            'question_text': request.POST.get('question_text'),
            'explanation': request.POST.get('explanation'),
            'author': request.user.teacher_profile,
            'question_image': request.FILES.get('question_image')
        }
        print(question_data)
        # Question.objects.create(**question_data)
        for number in range(1, NUMBER_OF_RESPONSES + 1):
            answer_data = {

            }
        context = {}
    return render(request, 'add_question.html', context=context)