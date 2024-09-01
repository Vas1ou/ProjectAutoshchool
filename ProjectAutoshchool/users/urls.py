from django.urls import path
from .views import registration, login_user, logout_user

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('login_user/', login_user, name='login_user'),
    path('logout_user/', logout_user, name='logout_user')
]