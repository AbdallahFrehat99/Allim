
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index ,name ='index'),  # Root path
    path('login', views.Login_page ,name ='Login'),  # Root path
    path('register', views.register_page ,name ='register'),  # Root path
    path('Reg_form', views.reg_form ,name ='registerForm'),  # Root path
    path('Login_form', views.Login_form ,name ='loginForm'),  # Root path
    path('teacher/dashboard',views.teacher_dashboard),
    path('student/dashboard',views.student_dashboard),
    

    ]
