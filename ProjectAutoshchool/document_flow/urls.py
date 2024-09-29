from django.urls import path
from .views import submit_documents, viewing_documents, accept_documents

urlpatterns = [
    path('submit/', submit_documents, name='submit_documents'),
    path('viewing/', viewing_documents, name='viewing_documents'),
    path('accept/<int:stud_id>/', accept_documents, name='accept_documents')
]