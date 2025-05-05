
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
    path('student_profile', views.student_profile, name='student_profile'),
    path('edit-profile-page',views.edit_student_page),
    path('edit-profile', views.edit_student_profile, name='edit_student_profile'),
    path('enroll_course',views.register_course),
    path('enroll_course/<int:course_id>', views.enroll_course, name='enroll_course'),
    path('delete_course/<int:c_id>',views.delete_course),
    path('teacher_profile', views.teacher_profile),
    path('edit_teacher_profile_page',views.edit_teacher_page),
    path('edit_teacher_profile', views.edit_teacher_profile),
    path('ajax/search_courses/', views.search_courses, name='search_courses'),
    path('add_lecture/<int:course_id>',views.add_lecture_page),
    path('add_lecture_to_course/<int:course_id>',views.add_lecture_to_course),
    path('show_lectures/<int:course_id>',views.show_lectures),
    path('lecture/<int:lecture_id>',views.get_lecture)

    ]
