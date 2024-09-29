from document_flow.models import DocumentsAdmission


# Это контекстный процессор, который добавляет переменную document_count во все представления
def doc_count_processor(request):
    try:
        if request.user.manager_profile:
            document_count = len(DocumentsAdmission.objects.filter(verified=False))
            return {'document_count': document_count}
    except Exception:
        return {}