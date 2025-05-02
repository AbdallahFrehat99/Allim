
from django.urls import path
from . import views


urlpatterns = [
    path('', views.index ,name ='index'),  # Root path
    path('register', views.register_user, name='register'),
    path('teacher/dashboard/', views.teacher_dashboard, name='teacher_dashboard'),
    path('student/dashboard/', views.student_dashboard, name='student_dashboard'),
]
