from django.urls import path
from .views import registration, login_user, logout_user, add_group, get_groups

urlpatterns = [
    path('registration/', registration, name='registration'),
    path('login_user/', login_user, name='login_user'),
    path('logout_user/', logout_user, name='logout_user'),
    path('add_group/', add_group, name='add_group'),
    path('get_groups/', get_groups, name='get_groups')
]