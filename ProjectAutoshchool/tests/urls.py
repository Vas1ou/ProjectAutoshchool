from django.urls import path
from .views import add_question, view_questions, question_detail

urlpatterns = [
    path('add_question/', add_question, name='add_question'),
    path('view_questions/', view_questions, name='view_questions'),
    path('question_detail/<int:question_id>/', question_detail, name='question_detail')
]