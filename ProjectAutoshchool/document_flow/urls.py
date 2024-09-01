from django.urls import path
from .views import submit_documents

urlpatterns = [
    path('submit/', submit_documents, name='submit_documents'),
]