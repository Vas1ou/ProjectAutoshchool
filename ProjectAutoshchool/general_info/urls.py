from django.urls import path
from .views import general, about_us

urlpatterns = [
    path('', general, name='general'),
    path('about_us/', about_us, name='about_us')
]