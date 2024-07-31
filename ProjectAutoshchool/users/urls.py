from django.urls import path
from .views import mytestview

urlpatterns = [
    path('', mytestview)
]