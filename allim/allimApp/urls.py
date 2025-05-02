
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index ,name ='index'),  # Root path
    path('login', views.Login_page ,name ='Login'),  # Root path
    path('register', views.register_page ,name ='register'),  # Root path
    ]
