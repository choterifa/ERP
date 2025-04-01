from django.urls import path
from . import views
from django.contrib.auth import views as auth_views
from .views import login_view, logout_view

app_name = 'usuarios'

urlpatterns = [
    path('login/', login_view, name='login'),
    path('logout/', logout_view, name='logout'),
]