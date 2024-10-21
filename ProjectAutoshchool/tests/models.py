from django.db import models
from users.models import TeacherProfile


class Question(models.Model):
    question_text = models.TextField(verbose_name='Текст вопроса')
    explanation = models.TextField(verbose_name='Текст пояснения к правильному ответу', blank=True, null=True)
    author = models.ForeignKey(TeacherProfile, on_delete=models.SET_NULL, blank=True, null=True, related_name='questions', verbose_name='Автор вопроса')
    question_image = models.ImageField(upload_to='questions/', blank=True, null=True, verbose_name='Изображение')

    def __str__(self):
        return f'Вопрос № {self.pk}.'


class Answer(models.Model):
    question = models.ForeignKey(Question, on_delete=models.CASCADE, related_name='answers')
    answer_text = models.CharField(verbose_name='Текст ответа', max_length=255)

    is_correct = models.BooleanField(default=False, verbose_name='Правильный ли ответ')

    def __str__(self):
        return f'{"Правильный" if self.is_correct else "Неправильный"} ответ на {self.question}'
