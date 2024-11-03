from lib2to3.fixes.fix_input import context

from django.shortcuts import render, redirect

from users.models import TeacherProfile
from .models import Question, Answer

# количество вариантов ответов
NUMBER_OF_RESPONSES = 4


def add_question(request):
    if request.method == 'GET':
        context = {
            'title': 'Создать вопрос',
            'number_of_responses': range(1, NUMBER_OF_RESPONSES + 1)
        }
        return render(request, 'add_question.html', context=context)
    elif request.method == 'POST':
        question_data = {
            'question_text': request.POST.get('question_text'),
            'explanation': request.POST.get('explanation'),
            'author': request.user.teacher_profile,
            'question_image': request.FILES.get('question_image')
        }
        question = Question.objects.create(**question_data)
        for number in range(1, NUMBER_OF_RESPONSES + 1):
            answer_text = request.POST.get(f'answer{number}')
            if answer_text:
                answer_data = {
                    'question': question,
                    'answer_text': answer_text,
                    'is_correct': True if request.POST.get(f'correct_answer{number}') else False
                }
                Answer.objects.create(**answer_data)
        return redirect('general')


def view_questions(request):
    teacher = request.GET.get('author')
    if teacher:
        if teacher == 'deleted_authors':
            questions = Question.objects.filter(author_id=None).prefetch_related('answers')
        else:
            questions = Question.objects.filter(author_id=teacher).prefetch_related('answers')
    else:
        questions = Question.objects.prefetch_related('answers').all()
    authors = TeacherProfile.objects.all()
    context = {
        'title': 'Просмотр вопросов',
        'questions': questions,
        'authors': authors
    }
    return render(request, 'view_questions.html', context=context)


def question_detail(request, question_id):
    question = Question.objects.prefetch_related('answers').get(id=question_id)
    answer_count = question.answers.count()
    if request.method == 'GET':
        return render(request, 'question_detail.html', {
            'title': 'Просмотр вопроса',
            'author': question.author.user.get_full_name() if question.author else 'Автор удалён',
            'question': question,
            'answer_count': range(answer_count + 1, NUMBER_OF_RESPONSES + 1) if answer_count < NUMBER_OF_RESPONSES else []
        })
