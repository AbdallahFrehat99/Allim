
from django.urls import path
from . import views
from .views import chatbot_view, get_bot_response  #Ai

urlpatterns = [
    path('', views.index ,name ='index'),  # Root path
    path('login', views.Login_page ,name ='Login'),  # Root path
    path('register', views.register_page ,name ='register'),  # Root path
    path('Reg_form', views.reg_form ,name ='registerForm'),  # Root path
    path('Login_form', views.Login_form ,name ='loginForm'),  # Root path
    path('teacher/dashboard',views.teacher_dashboard),
    path('student/dashboard',views.student_dashboard),
    path("chat/", chatbot_view, name="chatbot"),
    path("chat/api/", get_bot_response, name="chatbot_api"),
    path('logout',views.log_out),
    path('teacher/create_course',views.create_course_page),
    path('create_course',views.create_course),
    path('delete_course/<int:c_id>',views.delete_course)



    ]
